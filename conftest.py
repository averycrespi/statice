import pytest

from app import create_app, db
from app.config import TestingConfig
from app.models import Check, Status


@pytest.fixture
def app():
    """Create a application configured for testing."""
    return create_app(TestingConfig)


@pytest.fixture
def session(app):
    """Create a database session."""
    with app.app_context():
        db.create_all()
        yield db.session
        db.drop_all()


@pytest.fixture
def check():
    """Create a check."""
    return Check(name="Example", url="https://example.com", status=Status.INFO)
