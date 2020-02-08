from app import create_app, db
from app.config import DevConfig
from app.daemons.inquisitor import Inquisitor
from app.daemons.janitor import Janitor
from app.models import User


app = create_app(DevConfig)


@app.cli.command("create_user")
def create_user():
    """Create the default user."""
    username = app.config["STATICE_USERNAME"]
    password = app.config["STATICE_PASSWORD"]
    if User.query.filter_by(username=username).first():
        app.logger.info("Found existing user: %s", username)
    else:
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        app.logger.info("Created user: %s", username)


@app.cli.command("inquisitor")
def inquisitor():
    """Run the inquisitor."""
    inquisitor = Inquisitor(
        interval=app.config["STATICE_REQUEST_INTERVAL"],
        timeout=app.config["STATICE_REQUEST_TIMEOUT"],
    )
    inquisitor.run()


@app.cli.command("janitor")
def janitor():
    """Run the janitor."""
    janitor = Janitor(
        interval=app.config["STATICE_PURGE_INTERVAL"],
        age=app.config["STATICE_PURGE_AGE"],
    )
    janitor.run()
