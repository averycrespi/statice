from app import create_app, db
from app.config import Config
from app.daemon import Daemon
from app.models import Check, Response, Status


app = create_app(Config)


@app.cli.command("daemon")
def daemon():
    """Start the daemon."""
    daemon = Daemon()
    daemon.start()


@app.cli.command("seed")
def seed():
    """Seed the database."""
    codes = [100, 200, 300, 400, 500]

    with app.app_context():
        Response.query.delete()
        Check.query.delete()
        db.session.commit()

        checks = [
            Check(name=str(code), url=f"https://httpstat.us/{code}", status=Status.INFO)
            for code in codes
        ]
        db.session.add_all(checks)
        db.session.commit()
