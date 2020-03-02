import pytest

from app import create_app, db
from app.config import TestingConfig


@pytest.fixture
def app():
    return create_app(TestingConfig)


@pytest.fixture
def session(app):
    with app.app_context():
        db.create_all()
        yield db.session
        db.drop_all()
