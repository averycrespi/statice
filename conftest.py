import pytest

from app import create_app, db as app_db
from app.config import TestingConfig
from app.models import Check, Status


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
    return Check(name="Example", url="https://example.com", status=Status.INFO)
