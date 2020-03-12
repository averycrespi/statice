from datetime import datetime
import pytest

from app import create_app, db as app_db
from app.config import TestingConfig
from app.models import Check, Response, Status


@pytest.fixture
def app():
    """Create a application configured for testing."""
    return create_app(TestingConfig)


@pytest.fixture
def db(app):
    """Create a database connection."""
    with app.app_context():
        app_db.create_all()
        yield app_db
        app_db.drop_all()


@pytest.fixture
def check():
    """Create a check."""
    return Check(id=1, name="Example", url="https://example.com", status=Status.INFO)


@pytest.fixture
def response():
    """Create a response."""
    return Response(
        id=1,
        check_id=1,
        start_time=datetime.utcnow(),
        elapsed_ms=50,
        status=Status.SUCCESS,
        description="HTTP 200: OK",
    )
