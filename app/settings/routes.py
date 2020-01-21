from flask import render_template

from app.settings import bp


@bp.route("/settings")
def settings():
    return render_template("settings.html")
