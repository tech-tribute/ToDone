from todone import app
from flask import request, render_template, redirect, flash, url_for
from todone.models import *
from todone.forms import DatabaseForm
from werkzeug.utils import secure_filename
import os
from todone.utils import allowedFile
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from datetime import datetime
# Create Views/Urls/routes below


@app.route("/upload", methods=("POST",))
def upload():
    # check if the post request has the file part
    if "todo_list" not in request.files:
        flash("No file part", "error")
        return redirect(url_for("index"))
    file = request.files["todo_list"]

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        flash("No selected file", "error")
        return redirect(url_for("index"))

    if not allowedFile(file.filename):
        flash("You can upload only json files!", 'error')
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)
    file.save(os.path.join("project\\", app.config["UPLOAD_FOLDER"], filename))

    return redirect(url_for("todo", filename=filename))


@app.route("/", methods=("POST", "GET"))
def index():
    form = DatabaseForm()

    return render_template("index.html", form=form)

class TaskForm(FlaskForm):
    caption = StringField('Caption')
    submit = SubmitField('Add Task')


@app.route("/todo/<string:filename>", methods=("POST", "GET"))
@app.route("/todo", methods=("POST", "GET"))
@app.route("/todo")
def todo():
    task_manager = TaskManager("tasks_data.json")
    tasks = task_manager.query_all()
    completed_tasks = task_manager.query_done_tasks()
    active_filter = request.args.get("filter")
    form = TaskForm()
    if request.method == "POST":
        if form.validate_on_submit():
            caption = form.caption.data
            new_task = Task(id=len(tasks), caption=caption, create=datetime.now(), done=False)
            if not new_task.is_caption(caption):
                flash("Caption must contain more than 3 characters!", "error")
            else:
                try:
                    tasks.append(new_task)
                    task_manager.save_data_to_json(tasks)
                    flash("Task added successfully!", "success")
                except:
                    flash("Something went wrong during adding your task!", "error")

    return render_template(
        "todo.html",
        tasks=tasks,
        form= TaskForm(),
        completed_tasks=completed_tasks,
        active_filter=active_filter,
    )

    # ------------------------------------------------------


@app.route("/todo/delete/<int:id>")
def deleteTask(id):
    task_manager = TaskManager("tasks_data.json")

    task = task_manager.query_by_id(id)
    if task:
        task_manager.tasks.remove(task[0])
        task_manager.save_data_to_json()

    return redirect(url_for("todo"))
