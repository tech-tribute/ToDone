from flask_wtf import FlaskForm
from wtforms.fields import StringField, FileField, SubmitField, BooleanField
from wtforms.validators import DataRequired


# Write your Forms below :
class DatabaseForm(FlaskForm):
    todo_list = FileField(
        "todo_list",
    )


class TaskForm(FlaskForm):
    caption = StringField(
        "Caption",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "What needs to be done?",
            "autofocus": True,
            "class": "new-todo",
            "value": "",
        },
    )
    submit = SubmitField("Add Task")


class EditTaskForm(FlaskForm):
    caption = StringField(
        "Caption",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "Caption",
            "autofocus": True,
            "value": "",
        },
    )
    submit = SubmitField("Edit Task")
