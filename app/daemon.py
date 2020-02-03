from datetime import datetime
import http.client
from flask import current_app
import requests
from requests.exceptions import (
    ConnectionError,
    RequestException,
    Timeout,
    TooManyRedirects,
)

from app import db, rq
from app.models import Check, Event, Response, Status


class Daemon:
    def __init__(self):
        self.jobs = []

    def awaken(self):
        current_app.logger.info("Waking up")
        for job in self.jobs:
            if job.is_finished:
                self.jobs.remove(job)
                self.handle_finished(job)
            elif job.is_failed:
                self.jobs.remove(job)
                self.handle_failed(job)
        for check in Check.query.all():
            self.jobs.append(send_request.queue(check))

    def handle_finished(self, job):
        current_app.logger.info("Handling finished job: %s", str(job.id))
        response = job.result
        check = Check.query.filter_by(id=response.check_id).first()
        if check:
            current_app.logger.info("Updating check: %s", str(check))
            status = Status.SUCCESS if response.ok else Status.FAILURE
            check.status = status
            event = Event(
                check_id=check.id, message=response.description, status=status
            )
            db.session.add_all((check, event, response))
            db.session.commit()
        else:
            current_app.logger.warning("Check not found. Skipping ...")

    def handle_failed(self, job):
        # TODO: implement
        current_app.logger.warning("Handling failed job: %s", str(job.id))
        pass


@rq.job
def send_request(check):
    """Send a HTTP GET request."""
    start_time = datetime.utcnow()
    try:
        resp = requests.get(check.url, timeout=5)
        elapsed_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        ok = 200 <= resp.status_code < 400
        description = (
            f"HTTP {resp.status_code}: {http.client.responses[resp.status_code]}"
        )
    except ConnectionError as e:
        ok = False
        description = "Error: Connection failed"
    except Timeout as e:
        ok = False
        description = "Error: Request timed out"
    except TooManyRedirects as e:
        ok = False
        description = "Error: Too many redirects"
    except RequestException as e:
        ok = False
        description = f"Error: {str(e)}"
    finally:
        elapsed_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        return Response(
            check_id=check.id,
            start_time=start_time,
            elapsed_ms=elapsed_ms,
            ok=ok,
            description=description,
        )
