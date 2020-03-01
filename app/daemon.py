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

    def start(self):
        """Start the daemon.

        This function will block indefinitely.
        """
        current_jobs = {}
        next_jobs = {}
        while True:
            for check_id, job in current_jobs.items():
                if job.is_finished:
                    current_app.logger.info("Job for check: %s has finished", check_id)
                    check = Check.query.filter_by(id=job.result.check_id).first()
                    if check is not None:
                        check.status = job.result.status
                        db.session.add_all((check, job.result))
                elif job.is_failed:
                    current_app.logger.error("Job for check: %s has failed", check_id)
                else:
                    # Job is still running, so we should try again next iteration.
                    next_jobs[check_id] = job
            db.session.commit()
            for check in Check.query.all():
                # Only enqueue jobs that are not currently running.
                # This prevents backpressure if the workers are overloaded.
                if check.id not in next_jobs:
                    next_jobs[check.id] = send_request.queue(check, self.timeout)
            current_jobs = next_jobs
            next_jobs = {}
            time.sleep(self.interval)
