import os


class Config:
    """Configures the application."""

    STATICE_DAEMON_INTERVAL = os.environ.get("STATICE_DAEMON_INTERVAL") or 10
    STATICE_REQUEST_TIMEOUT = os.environ.get("STATICE_REQUEST_TIMEOUT") or 3

    SECRET_KEY = os.environ.get("SECRET_KEY") or "change-me"

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
