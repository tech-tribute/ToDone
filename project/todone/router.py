from todone import app, db
from flask import request, render_template, redirect, flash, url_for
from todone.models import *
from todone.forms import CreateTaskForm, DatabaseForm

# Create Views/Urls/routes below


@app.route("/", methods=("POST", "GET"))
def index():
    # Create a form and then return it to the template to use it
    form = DatabaseForm()
    return render_template("index.html", form=form)


@app.route("/todo", methods=("POST", "GET"))
def todo():
    # If request of method is GET program will catch data from database and show them to user via rendering a template
    # If request of method is POST program will catch data and save them into database and render the template again

    # Create a form and then return it to the template to use it
    form = CreateTaskForm()
    if request.method == "POST":
        if not form.validate_on_submit():
            # Message of flash will save in SessionCookie, we can use that in template to show errors and warnings to the user
            flash("Data is wrong!!", "error")
            return redirect(url_for("todo"))

        # Extracting information from
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

    # Getting all of the tasks from database (We need to show them to user)
    tasks = Task.query.all()

    # Getting all of the completed tasks from database
    completed_tasks = Task.query.filter(Task.done == True).all()

    # In localhost/todo/ The user can choose the filter with which the tasks will be displayed, and we get the type of filtering using the GET method.
    active_filter = request.args.get("filter")

    # Rendering the final template with values we want!
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
