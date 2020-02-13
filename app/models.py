from datetime import datetime

from app import db


class Check(db.Model):  # type: ignore
    """Represents a URL check."""

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(), unique=True)
    url = db.Column(db.String())
    status = db.Column(db.String())

    responses = db.relationship("Response")

    def __repr__(self):
        return f"Check({self.name}, {self.url}, {self.status})"


class Response(db.Model):  # type: ignore
    """Represents an HTTP response."""

    id = db.Column(db.Integer, primary_key=True)
    check_id = db.Column(db.Integer, db.ForeignKey("check.id"))

    start_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    elapsed_ms = db.Column(db.Integer)
    status = db.Column(db.String())
    description = db.Column(db.String())

    def __lt__(self, other):
        # Sort responses by start time.
        return self.start_time < other.start_time

    def __repr__(self):
        return f"Response({self.start_time}, {self.elapsed_ms}, {self.status}, {self.description})"


class Status:
    """Represents Bootstrap alert levels."""

    INFO = "info"
    WARNING = "warning"
    FAILURE = "danger"
    SUCCESS = "success"


class Card:
    """Wraps a check into a Bootstrap card."""

    def __init__(self, check):
        self.check = check
        self.recent = sorted(check.responses, reverse=True)[:3]
