from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Log a user in."""

    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")
