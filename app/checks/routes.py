from flask import render_template, redirect, url_for, flash

from app import db
from app.checks import bp
from app.checks.forms import CreateOutboundCheckForm, DeleteOutboundCheckForm
from app.models import OutboundCheck


@bp.route("/view/outbound/<id>")
def view_outbound_check(id):
    check = OutboundCheck.query.filter_by(id=id).first()
    return render_template("view_outbound_check.html", outbound_check=check)


@bp.route("/create/outbound", methods=["GET", "POST"])
def create_outbound_check():
    form = CreateOutboundCheckForm()
    if form.validate_on_submit():
        check = OutboundCheck(name=form.name.data, url=form.url.data)
        db.session.add(check)
        db.session.commit()
        flash(
            "Outbound check {name} has been created.".format(name=form.name.data),
            "info",
        )
        return redirect(url_for("dashboard.dashboard"))
    return render_template("create_outbound_check.html", form=form)


@bp.route("/delete/outbound/<id>", methods=["GET", "POST"])
def delete_outbound_check(id):
    check = OutboundCheck.query.filter_by(id=id).first()
    if not check:
        flash("Check not found.", "warning")
        return redirect(url_for("dashboard.dashboard"))
    form = DeleteOutboundCheckForm()
    if form.validate_on_submit():
        db.session.delete(check)
        db.session.commit()
        flash("Outbound check {name} has been deleted.".format(name=check.name), "info")
        return redirect(url_for("dashboard.dashboard"))
    return render_template(
        "delete_outbound_check.html", form=form, outbound_check=check
    )
