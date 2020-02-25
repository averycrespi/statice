from app import create_app
from app.config import Config
from app.daemon import Daemon


app = create_app(Config)


@app.cli.command("daemon")
def daemon():
    """Run the daemon."""
    daemon = Daemon()
    daemon.start(
        interval=app.config["STATICE_DAEMON_INTERVAL"],
        timeout=app.config["STATICE_REQUEST_TIMEOUT"],
    )
