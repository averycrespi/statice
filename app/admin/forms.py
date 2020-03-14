from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
    ValidationError,
    URL,
)

from app.models import Check


class BaseCheckForm(FlaskForm):
    """Base class for check-related forms."""

    name = StringField("Name", validators=[DataRequired()])
    url = StringField("URL", validators=[DataRequired(), URL(), Length(max=2048)],)


class CreateCheckForm(BaseCheckForm):
    """Create a new check."""

    submit = SubmitField("Create")

    def validate_name(self, name):
        if Check.query.filter_by(name=name.data).first() is not None:
            raise ValidationError("Please enter a unique name.")


class EditCheckForm(BaseCheckForm):
    """Edit a check."""

    submit = SubmitField("Save")


class DeleteCheckForm(FlaskForm):
    """Delete a check."""

    name = StringField(
        "Enter the check name to confirm deletion", validators=[DataRequired()]
    )
    submit = SubmitField("Delete")
