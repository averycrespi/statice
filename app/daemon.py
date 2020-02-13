from flask import current_app
import time

from app import db
from app.models import Check
from app.jobs import send_request


class Daemon:
    """Run background tasks."""

    def __init__(self):
        self.interval = current_app.config["STATICE_DAEMON_INTERVAL"]
        self.timeout = current_app.config["STATICE_REQUEST_TIMEOUT"]
        self.jobs = []

    def start(self):
        """Start the daemon."""
        # TODO: implement non-blocking wait
        # TODO: make requests in parallel
        current_app.logger.info(
            f"Starting daemon with interval {self.interval} and timeout {self.timeout}"
        )
        while True:
            current_app.logger.info("Waking up ...")
            self.process_responses()
            self.enqueue_requests()
            current_app.logger.info("Going back to sleep ...")
            time.sleep(self.interval)

    def process_responses(self):
        """Proccess HTTP responses from the queue."""
        current_app.logger.info("Processing responses ...")
        for job in self.jobs:
            if job.is_finished:
                self.jobs.remove(job)
                response = job.result
                check = Check.query.filter_by(id=response.check_id).first()
                if check is not None:
                    check.status = response.status
                    db.session.add(check)
                    db.session.add(response)
                    db.session.commit()
            elif job.is_failed:
                self.jobs.remove(job)

    def enqueue_requests(self):
        """Add HTTP requests to the queue."""
        current_app.logger.info("Enqueuing requests ...")
        for check in Check.query.all():
            job = send_request.queue(check, self.timeout)
            self.jobs.append(job)
