from flask import current_app

from app import db
from app.jobs import send_request
from app.models import Check, Event


class Daemon:
    """Performs background tasks for the application."""

    def __init__(self):
        self.jobs = []

    def awaken(self):
        current_app.logger.info("Waking up ...")

        current_app.logger.info("Processing jobs ...")
        for job in self.jobs:
            if job.is_finished:
                self.jobs.remove(job)
                response = job.result
                event = Event.from_response(response)
                check = Check.query.filter_by(id=response.check_id).first()
                if check is not None:
                    current_app.logger.info("Updating check: {} ...".format(check.name))
                    check.status = event.status
                    db.session.add_all((response, event, check))
                    db.session.commit()

            elif job.is_failed:
                # TODO: handle failed jobs
                self.jobs.remove(job)

        current_app.logger.info("Enqueuing requests ...")
        for check in Check.query.all():
            self.jobs.append(
                send_request.queue(check, current_app.config["STATICE_TIMEOUT"])
            )

        current_app.logger.info("Going back to sleep ...")
