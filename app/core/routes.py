from flask import render_template

from app.core import bp


@bp.route("/")
@bp.route("/dashboard")
def dashboard():
    from collections import namedtuple

    Check = namedtuple("Check", ("name", "ok", "url", "last_updated"))
    checks = {
        Check(
            name="Plex",
            ok=True,
            url="plex.averycrespi.com",
            last_updated="3 seconds ago",
        ),
        Check(
            name="FTP", ok=False, url="ftp.averycrespi.com", last_updated="10 hours ago"
        ),
    }

    return render_template("dashboard.html", outbound_checks=checks)
