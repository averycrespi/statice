from flask import current_app
import time

from app import db
from app.models import Check
from app.jobs import send_request


class Daemon:
    """Run background tasks."""

    def __init__(self, *, interval=10, timeout=5):
        """Create a new daemon."""
        self.interval = interval
        self.timeout = timeout
        self.jobs = []

    def start(self):
        """Start the daemon."""
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
                # Ensure that the check still exists (i.e. wasn't deleted).
                # TODO: prevent potential ID conflict
                if check is not None:
                    check.status = response.status
                    db.session.add(check)
                    db.session.add(response)
            elif job.is_failed:
                current_app.logger.error("Job failed: {}".format(str(job)))
                self.jobs.remove(job)
        db.session.commit()

    def enqueue_requests(self):
        """Add HTTP requests to the queue."""
        current_app.logger.info("Enqueuing requests ...")
        # TODO: prevent backpressure
        for check in Check.query.all():
            job = send_request.queue(check, self.timeout)
            self.jobs.append(job)
