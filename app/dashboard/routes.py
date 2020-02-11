from flask import render_template

from app.checks import Card, Check
from app.dashboard import bp


@bp.route("/")
@bp.route("/dashboard")
def dashboard():
    """View the dashboard."""
    cards = [Card(check) for check in Check.query.all()]
    return render_template("dashboard.j2", cards=cards)
