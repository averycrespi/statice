from datetime import datetime
from flask import current_app
import requests

from app import db, rq
from app.models import Check, Event, Response, Status


class Daemon:
    def __init__(self):
        self.jobs = []

    def awaken(self):
        for job in self.jobs:
            if job.is_finished:
                current_app.logger.info("Handling result: %s", str(job.result))
                self.jobs.remove(job)

                response = job.result
                status = (
                    Status.SUCCESS
                    if 200 <= response.status_code < 400
                    else Status.FAILURE
                )
                check = Check.query.filter_by(id=response.check_id).first()
                check.status = status
                event = Event(
                    check_id=check.id,
                    status=status,
                    message=f"HTTP response {response.status_code}",
                )

                db.session.add_all([check, event, response])
                db.session.commit()
            elif job.is_failed:
                # TODO: handle failure
                self.jobs.remove(job)

        checks = Check.query.all()
        for check in checks:
            self.jobs.append(send_request.queue(check))


@rq.job
def send_request(check):
    start = datetime.utcnow()
    # TODO: handle timeouts
    resp = requests.get(check.url)
    end = datetime.utcnow()
    return Response(
        check_id=check.id, start_time=start, end_time=end, status_code=resp.status_code
    )
