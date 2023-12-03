from todone import app, db
from flask import request, render_template, redirect, flash, url_for
from todone.models import *
from todone.forms import CreateTaskForm, DatabaseForm
from werkzeug.utils import secure_filename
import os
from todone.utils import allowedFile, now


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
    # Create a form and then return it to the template to use it
    form = DatabaseForm()

    return render_template("index.html", form=form)


@app.route("/todo/<string:filename>", methods=("POST", "GET"))
@app.route("/todo", methods=("POST", "GET"))
def todo(filename=None):
    form = CreateTaskForm()

    if request.method == "POST":
        if not form.validate_on_submit():
            # Message of flash will save in SessionCookie,
            # we can use that in template to show errors and warnings to the user
            flash("Data is wrong!!", "error")
            return redirect(url_for("todo"))

        # Extracting information from form
        caption = form.caption.data

        # Create an object of Task Table in db (It must be committed to save the changes)
        new_task = Task(caption=caption)

        # Validating data
        if not new_task.is_caption(caption):
            flash("Caption must contain more that 3 characters!", "error")
            return redirect(url_for("todo"))

        try:
            # Saving database changes
            db.session.add(new_task)
            db.session.commit()
        except:
            flash("Something went wrong during adding your task!", "error")
            return redirect(url_for("todo"))

    # Address of route directory (TODONE)
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # ------------------------------------------------------ 
    # In development

    # if no file chosen
    if not filename:
        # making path
        filename = f"{now()}.json"
        filepath = os.path.join(ROOT_DIR, f"{app.config['UPLOAD_FOLDER']}\{filename}")

        # create a json file
        open(filepath, "x")
        return redirect(url_for("todo", filename=filename))

    # if file is not in db folder
    filepath = os.path.join(ROOT_DIR, f"{app.config['UPLOAD_FOLDER']}\{filename}")
    if filename and not os.path.isfile(filepath):
        flash(f"There is no such a file named : {filename}")
        return redirect("index")
    # ------------------------------------------------------

    # All of the tasks
    tasks = Task.query.all()

    # All of the completed tasks
    completed_tasks = Task.query.filter(Task.done == True).all()

    # In localhost/todo/ The user can choose the filter with which
    # the tasks will be displayed, and we get the type of filtering using the GET method.
    active_filter = request.args.get("filter")


    return render_template(
        "todo.html",
        tasks=tasks,
        form=form,
        completed_tasks=completed_tasks,
        active_filter=active_filter,
    )


@app.route("/todo/delete/<int:id>")
def deleteTask(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for("todo"))
