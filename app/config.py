import os


class Config:
    """Configures the application for Docker."""

    # Configure application-specific behaviour.
    STATICE_DAEMON_INTERVAL = int(os.environ.get("STATICE_DAEMON_INTERVAL") or 30)
    STATICE_REQUEST_TIMEOUT = int(os.environ.get("STATICE_REQUEST_TIMEOUT") or 5)
    STATICE_RESPONSES_PER_PAGE = int(os.environ.get("STATICE_RESPONSES_PER_PAGE") or 10)
    STATICE_MAX_CHART_SIZE = int(os.environ.get("STATICE_MAX_CHART_SIZE") or 25)

    # Configure Flask.
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(24).hex()

    # Configure PostgreSQL.
    POSTGRES_URL = os.environ.get("POSTGRES_URL") or "statice_db:5432"
    POSTGRES_DB = os.environ.get("POSTGRES_DB") or "postgres"
    POSTGRES_USER = os.environ.get("POSTGRES_USER") or "postgres"
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD") or "postgres"

    # Configure SQLAlchemy.
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{user}:{pw}@{url}/{db}".format(
        user=POSTGRES_USER, pw=POSTGRES_PASSWORD, url=POSTGRES_URL, db=POSTGRES_DB
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configure Redis.
    RQ_REDIS_URL = os.environ.get("REDIS_URL") or "redis://statice_redis:6379/0"
    RQ_QUEUES = ("default",)


class TestingConfig(Config):
    """Configures the application for testing."""

    # Use an in-memory SQLite database.
    SQLALCHEMY_DATABASE_URI = "sqlite://"

    # Enable testing.
    TESTING = True
    WTF_CSRF_ENABLED = False
