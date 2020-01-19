from flask import render_template

from app import db
from app.dashboard import bp
from app.models import OutboundCheck


@bp.route("/")
@bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", outbound_checks=OutboundCheck.query.all())
