import arrow
from flask import abort, flash, render_template

from app.models import Card, Check, Status
from app.dashboard import bp


@bp.route("/")
@bp.route("/dashboard")
def dashboard():
    """View the dashboard."""
    cards = [Card(check) for check in sorted(Check.query.all())]
    if len(cards) == 0:
        flash("No checks found.", category=Status.WARNING)
    return render_template("dashboard.j2", cards=cards)


@bp.route("/checks/<id>")
def view_check(id):
    """View a check by ID."""
    check = Check.query.filter_by(id=id).first()
    if check is None:
        abort(404)
    responses = sorted(check.responses)[-25:]
    return render_template(
        "view_check.j2",
        check=check,
        legend="Response Time (ms)",
        labels=[arrow.get(r.start_time).humanize() for r in responses],
        values=[r.elapsed_ms for r in responses],
    )
