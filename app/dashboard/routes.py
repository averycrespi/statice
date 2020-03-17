from flask import abort, current_app, flash, render_template, request

from app.models import Card, Chart, Check, Response, Status
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
    page = request.args.get("page", 1, type=int)
    pagination = check.responses.order_by(Response.start_time.desc()).paginate(
        page, current_app.config["STATICE_RESPONSES_PER_PAGE"], False
    )
    return render_template(
        "view_check.j2",
        check=check,
        chart=Chart(check, max_size=current_app.config["STATICE_MAX_CHART_SIZE"]),
        pagination=pagination,
    )
