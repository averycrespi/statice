from datetime import datetime, timedelta
from flask import current_app
import time

from app import db
from app.models import Event, Response


class Janitor:
    """Purge old events and responses."""

    def __init__(self, *, interval, age):
        self.interval = interval
        self.age = age

    def run(self):
        current_app.logger.info(
            f"Running janitor with interval: {self.interval} and age: {self.age}"
        )
        while True:
            self.wake_up()
            time.sleep(self.interval)

    def wake_up(self):
        current_app.logger.info("Waking up ...")

        current_app.logger.info("Purging old events and responses ...")
        cutoff = datetime.utcnow() - timedelta(seconds=self.age)
        num_events = Event.query.filter(Event.time < cutoff).delete()
        num_responses = Response.query.filter(Response.start_time < cutoff).delete()
        db.session.commit()

        current_app.logger.info(
            f"Deleted {num_events} events and {num_responses} responses"
        )

        current_app.logger.info("Going back to sleep ...")
