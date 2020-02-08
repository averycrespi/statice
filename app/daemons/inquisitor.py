from flask import current_app

import time

from app import db
from app.jobs import send_request
from app.models import Check, Event


class Inquisitor:
    """Send requests and handle responses."""

    def __init__(self, *, interval, timeout):
        self.interval = interval
        self.timeout = timeout
        self.jobs = []

    def run(self):
        current_app.logger.info(
            f"Running inquisitor with interval: {self.interval} and timeout: {self.timeout}"
        )
        while True:
            self.wake_up()
            time.sleep(self.interval)

    def wake_up(self):
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
                self.jobs.remove(job)
                current_app.logger.error(f"Job failed: {str(job)}")

        current_app.logger.info("Enqueuing requests ...")
        for check in Check.query.all():
            self.jobs.append(send_request.queue(check, self.timeout))

        current_app.logger.info("Going back to sleep ...")
