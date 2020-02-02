import redis
from rq import Connection, Worker
import time

from app import create_app, db
from app.config import DevConfig
from app.daemon import wake_up
from app.models import User


app = create_app(DevConfig)


@app.cli.command("create_user")
def create_user():
    """Create the default user."""
    username = app.config["STATICE_USERNAME"]
    password = app.config["STATICE_PASSWORD"]
    if User.query.filter_by(username=username).first():
        app.logger.info("found existing user: %s", username)
    else:
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        app.logger.info("created user: %s", username)


@app.cli.command("run_worker")
def run_worker():
    """Run a Redis worker."""
    conn = redis.from_url(app.config["REDIS_URL"])
    with Connection(conn):
        worker = Worker(app.config["REDIS_QUEUES"])
        worker.work()


@app.cli.command("run_daemon")
def run_daemon():
    """Run the daemon."""
    while True:
        wake_up()
        time.sleep(5)
