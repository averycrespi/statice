from flask import render_template, redirect, url_for, flash

from app import db
from app.checks import bp
from app.checks.forms import CreateOutboundCheckForm
from app.models import OutboundCheck


@bp.route("/create/outbound", methods=["GET", "POST"])
def create_outbound_check():
    form = CreateOutboundCheckForm()
    if form.validate_on_submit():
        check = OutboundCheck(name=form.name.data, url=form.url.data)
        db.session.add(check)
        db.session.commit()
        flash("Outbound check {} has been created!".format(form.name.data), "info")
        return redirect(url_for("dashboard.dashboard"))
    return render_template("create_outbound_check.html", form=form)
