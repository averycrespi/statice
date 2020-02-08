from flask import render_template


def page_not_found(e):
    """Handle Page Not Found error."""
    return render_template("404.j2"), 404
