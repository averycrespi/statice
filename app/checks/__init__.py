from flask import Blueprint


bp = Blueprint("checks", __name__, template_folder="templates")


from app.checks import routes
