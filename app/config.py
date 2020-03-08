import os


class Config:
    """Configures the application for development or production."""

    # Configure application-specific behaviour.
    STATICE_DAEMON_INTERVAL = int(os.environ.get("STATICE_DAEMON_INTERVAL") or 30)
    STATICE_REQUEST_TIMEOUT = int(os.environ.get("STATICE_REQUEST_TIMEOUT") or 5)

    # If a secret key is not set, generate a random key on startup.
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(24).hex()

    POSTGRES_URL = os.environ.get("POSTGRES_URL") or "localhost:5432"
    POSTGRES_DB = os.environ.get("POSTGRES_DB") or "postgres"
    POSTGRES_USER = os.environ.get("POSTGRES_USER") or "postgres"
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD") or "postgres"

    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{user}:{pw}@{url}/{db}".format(
        user=POSTGRES_USER, pw=POSTGRES_PASSWORD, url=POSTGRES_URL, db=POSTGRES_DB
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RQ_REDIS_URL = os.environ.get("REDIS_URL") or "redis://localhost:6379/0"
    RQ_QUEUES = ("default",)


class TestingConfig(Config):
    """Configures the application for testing."""

    # Use an in-memory SQLite database.
    SQLALCHEMY_DATABASE_URI = "sqlite://"

    TESTING = True
    WTF_CSRF_ENABLED = False
