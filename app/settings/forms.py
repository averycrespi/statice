from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class CreateCheckForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    url = StringField("URL", validators=[DataRequired()])
    interval = StringField("Interval")
    submit = SubmitField("Create")

    def validate_name(self, name):
        if Check.query.filter_by(name=name.data).first() is not None:
            raise ValidationError("Please use a unique check name.")
