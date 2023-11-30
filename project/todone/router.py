from todone import app, db
from flask import request, render_template, redirect, flash, url_for
from todone.models import *
from todone.forms import CreateTaskForm, DatabaseForm

# URLS :


@app.route("/", methods=("POST", "GET"))
def index():
    form = DatabaseForm()
    return render_template("index.html", form=form)


@app.route("/todo", methods=("POST", "GET"))
def todo():
    form = CreateTaskForm()
    if request.method == "POST":
        if not form.validate_on_submit():
            flash("Data is wrong!!")
            return redirect(url_for("todo"))
        
        caption = form.caption.data
        new_task = Task(caption=caption)

        if not new_task.is_caption(caption):
            flash("Caption mush contain more that 3 characters!")
            return redirect(url_for("todo"))
        
        try:
            db.session.add(new_task)
            db.session.commit()
        except:
            flash("Something went wrong during adding your task!")
            return redirect(url_for("todo"))

    tasks = Task.query.all()
    completed_tasks = Task.query.filter(Task.done==True).all()
    active_filter = request.args.get("filter")
    print(active_filter)
    return render_template("todo.html", tasks=tasks, form=form, completed_tasks=completed_tasks, active_filter=active_filter)
