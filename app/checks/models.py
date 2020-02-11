from datetime import datetime

from app import db


class Check(db.Model):  # type: ignore
    """Represents a check."""

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(), unique=True)
    url = db.Column(db.String())
    status = db.Column(db.String())

    events = db.relationship("Event")
    responses = db.relationship("Response")

    def __repr__(self):
        return f"Check({self.name}, {self.url}, {self.status})"


class Event(db.Model):  # type: ignore
    """Represents an event."""

    id = db.Column(db.Integer, primary_key=True)
    check_id = db.Column(db.Integer, db.ForeignKey("check.id"))

    time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    message = db.Column(db.String())
    status = db.Column(db.String())

    def __lt__(self, other):
        # Sort events by timestamp.
        return self.time < other.time

    def __repr__(self):
        return f"Event(time={self.time}, message={self.message}, status={self.status})"

    @staticmethod
    def from_response(response):
        return Event(
            check_id=response.check_id,
            time=response.start_time,
            message=response.description,
            status=Status.SUCCESS if response.ok else Status.FAILURE,
        )


class Response(db.Model):  # type: ignore
    """Represents a response."""

    id = db.Column(db.Integer, primary_key=True)
    check_id = db.Column(db.Integer, db.ForeignKey("check.id"))

    start_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    elapsed_ms = db.Column(db.Integer)
    ok = db.Column(db.Boolean)
    description = db.Column(db.String())

    def __lt__(self, other):
        # Sort responses by start time.
        return self.start_time < other.start_time

    def __repr__(self):
        return f"Response({self.start_time}, {self.elapsed_ms}, {self.ok}, {self.description})"


class Status:
    """Maps stasuses to Bootstrap alert levels."""

    INFO = "info"
    WARNING = "warning"
    FAILURE = "danger"
    SUCCESS = "success"


class Card:
    """Wraps a check into a Bootstrap card."""

    def __init__(self, check):
        self.check = check
        self.recent_events = sorted(check.events, reverse=True)[:3]
