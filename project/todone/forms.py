from flask_wtf import FlaskForm
from wtforms.fields import StringField, FileField
from wtforms.validators import DataRequired


# Write your Forms below :

class CreateTaskForm(FlaskForm):
    caption = StringField(
        "caption",
        validators=[DataRequired()],

        # Attributes of the <input>
        render_kw={"placeholder": "What needs to be done?", "autofocus": True, "class":"new-todo", "value":""},
    )


class DatabaseForm(FlaskForm):
    todo_list = FileField("todo_list",)
