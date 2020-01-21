from flask import render_template

from app.dashboard import bp
from app.models import Check


@bp.route("/")
@bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", checks=Check.query.all())
