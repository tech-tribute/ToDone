from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import DataRequired


class CreateTaskForm(FlaskForm):
    caption = StringField("caption", [DataRequired()])
