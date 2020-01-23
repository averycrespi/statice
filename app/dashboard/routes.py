from flask import current_app, render_template
from sqlalchemy import desc

from app.dashboard import bp
from app.models import Check, Event


@bp.route("/")
@bp.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        checks=Check.query.all(),
        events=Event.query.order_by(desc(Event.timestamp)).limit(10).all(),
    )
