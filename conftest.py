import pytest

from app import create_app
from app.config import TestingConfig


@pytest.fixture
def app():
    return create_app(TestingConfig)
