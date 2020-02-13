from flask import abort, current_app, flash, redirect, render_template, url_for

from app import db
from app.admin import bp
from app.admin.forms import CreateCheckForm, DeleteCheckForm, EditCheckForm
from app.models import Check, Status


@bp.route("/checks", methods=["GET", "POST"])
def manage_checks():
    """Manage checks."""
    return render_template("manage_checks.j2", checks=Check.query.all())


@bp.route("/checks/create", methods=["GET", "POST"])
def create_check():
    """Create a new check."""
    form = CreateCheckForm()
    if form.validate_on_submit():
        check = Check(name=form.name.data, url=form.url.data, status=Status.INFO,)
        db.session.add(check)
        db.session.commit()
        flash(f"Check {check.name} has been created.", category=Status.INFO)
        current_app.logger.info("Created check: %s", str(check))
        return redirect(url_for("admin.manage_checks"))
    return render_template("create_check.j2", create_form=form)


@bp.route("/checks/edit/<id>", methods=["GET", "POST"])
def edit_check(id):
    """Edit a check by ID."""
    check = Check.query.filter_by(id=id).first()
    if check is None:
        abort(404)
    form = EditCheckForm(obj=check)
    if form.validate_on_submit():
        if form.cancel.data:
            return redirect(url_for("admin.manage_checks"))
        check.name = form.name.data
        check.url = form.url.data
        db.session.add(check)
        db.session.commit()
        flash(f"Check {check.name} has been saved.", category=Status.INFO)
        current_app.logger.info("Saved check: %s", str(check))
        return redirect(url_for("admin.manage_checks"))
    return render_template("edit_check.j2", edit_form=form)


@bp.route("/checks/delete/<id>", methods=["GET", "POST"])
def delete_check(id):
    """Delete a check by ID."""
    check = Check.query.filter_by(id=id).first()
    if check is None:
        abort(404)
    form = DeleteCheckForm()
    if form.validate_on_submit():
        if form.cancel.data:
            return redirect(url_for("admin.manage_checks"))
        # TODO: implement cascade deletion
        db.session.delete(check)
        db.session.commit()
        flash(f"Check {check.name} has been deleted.", category=Status.WARNING)
        current_app.logger.warning("Deleted check: %s", str(check))
        return redirect(url_for("admin.manage_checks"))
    return render_template("delete_check.j2", check=check, delete_form=form)
