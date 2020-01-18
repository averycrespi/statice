from flask import render_template

from app.core import bp


@bp.route("/")
def dashboard():
    return render_template("dashboard.html")
