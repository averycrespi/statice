from flask import render_template

from app.core import bp


@bp.route("/")
@bp.route("/dashboard")
def dashboard():
    checks = {
        "foo": True,
        "bar": False,
    }
    return render_template("dashboard.html", checks=checks)
