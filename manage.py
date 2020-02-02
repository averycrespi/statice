import time

from app import create_app, db
from app.config import DevConfig
from app.daemon import Daemon
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


@app.cli.command("daemon")
def daemon():
    """Run the daemon."""
    # TODO: don't block
    interval = app.config["STATICE_INTERVAL"]
    daemon = Daemon()
    while True:
        daemon.awaken()
        time.sleep(interval)
