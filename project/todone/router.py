from flask import request, render_template, redirect, flash, url_for, send_file
from werkzeug.utils import secure_filename
from datetime import datetime
import os

from todone.models import *
from todone.forms import DatabaseForm, TaskForm, EditTaskForm
from todone.utils import (
    allowedFile,
    generate_numeric_id,
    create_json,
    generate_json_path,
    filter_by,
)
from todone import app


# Create Views/Urls/routes here.


@app.route("/", methods=("POST", "GET"))
def index():
    # Create a form and then return it to the template to use it
    form = DatabaseForm()

    todo_lists = os.listdir("project/db")

    return render_template("index.html", form=form, todo_lists=todo_lists)


@app.route("/todo/<string:filename>", methods=("POST", "GET"))
@app.route("/todo/", methods=("GET",))
def todo(filename: str = None):
    # if no file chosen
    if not filename:
        filename = create_json()
        return redirect(url_for("todo", filename=filename))

    # if file is not in db folder
    filepath = generate_json_path(filename)
    if filename and not os.path.isfile(filepath):
        flash(f"There is no such a file named : {filename}")
        return redirect(url_for("index"))

    form = TaskForm()
    # To do CRUD operations on json file
    task_manager = TaskManager(filepath)

    if request.method == "POST":
        if form.validate_on_submit():
            caption = form.caption.data
            id = generate_numeric_id()
            new_task = Task(id=id, caption=caption, create=datetime.now(), done=False)

            if not new_task.is_caption(caption):
                flash("Caption must contain more than 3 characters!", "error")
                return redirect(url_for("todo", filename=filename))

            task_manager.tasks.append(new_task)
            task_manager.save_data_to_json()
            return redirect(url_for("todo", filename=filename))

    filter_ = request.args.get("filter")
    tasks = filter_by(filter_, task_manager)
    tasks_not_done = task_manager.query_undone_tasks()

    return render_template("todo.html", tasks=tasks, form=form, filename=filename, tasks_not_done=tasks_not_done)


@app.route("/todo/<string:filename>/delete/<int:id>")
def deleteTask(filename, id):
    filepath = generate_json_path(filename)
    task_manager = TaskManager(filepath)

    task = task_manager.query_by_id(id)
    if task:
        task_manager.tasks.remove(task[0])
        task_manager.save_data_to_json()

    return redirect(url_for("todo", filename=filename))


@app.route("/todo/<string:filename>/clear/")
def clearCompleted(filename):
    filepath = generate_json_path(filename)
    task_manager = TaskManager(filepath)

    tasks = task_manager.query_done_tasks()
    for task in tasks:
        task_manager.tasks.remove(task)
        task_manager.save_data_to_json()

    return redirect(url_for("todo", filename=filename))


@app.route("/upload/", methods=("POST",))
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
        flash("You can upload only json files!", "error")
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)
    file.save(os.path.join("project\\", app.config["UPLOAD_FOLDER"], filename))

    return redirect(url_for("todo", filename=filename))


@app.route("/todo/<string:filename>/edit/<int:id>/", methods=("GET", "POST",))
def edit(filename: str, id: int):
    # if file is not in db folder
    filepath = generate_json_path(filename)
    if filename and not os.path.isfile(filepath):
        flash(f"There is no such a file named : {filename}")
        return redirect(url_for("index"))

    form = EditTaskForm()
    # To do CRUD operations on json file
    task_manager = TaskManager(filepath)

    if request.method == "POST":
        if form.validate_on_submit():
            task = task_manager.query_by_id(id)[0]
            caption = form.caption.data

            new_task = Task(id=id, caption=caption, create=task.create, done=task.done)
            if not new_task.is_caption(caption):
                flash("Caption must contain more than 3 characters!", "error")
                return redirect(url_for("edit", filename=filename, id=id))

            task_manager.tasks[task_manager.tasks.index(task)] = new_task
            task_manager.save_data_to_json()
            return redirect(url_for("todo", filename=filename))


    return render_template("edit.html", form=form, filename=filename, id=id)

@app.route("/download/<string:filename>")
def download(filename):
    s = generate_json_path(filename)
    return send_file(s, as_attachment=True)
