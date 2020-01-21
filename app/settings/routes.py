from flask import redirect, render_template, url_for

from app import db
from app.models import Check
from app.settings import bp
from app.settings.forms import CreateCheckForm


@bp.route("/settings", methods=["GET", "POST"])
def settings():
    form = CreateCheckForm()
    if form.validate_on_submit():
        check = Check(name=form.name, url=form.url)
        db.session.add(check)
        db.session.commit()
        flash(f"Check '{check.name}' has been created.")
        return redirect(url_for("settings.settings"))
    return render_template("settings.html", checks=Check.query.all(), form=form)
