from flask import render_template

from app.dashboard import bp
from app.models import Check


@bp.route("/")
@bp.route("/dashboard")
def dashboard():
    checks = Check.query.all()
    for check in checks:
        # TODO: refactor magic number
        check.recent_events = sorted(check.events, reverse=True)[:3]
    return render_template("dashboard.html", checks=checks)
