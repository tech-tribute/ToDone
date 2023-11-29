from todone import app, db
from flask import request, render_template, redirect, session, flash, url_for
from todone.models import *
from todone.forms import CreateTaskForm

# URLS :


@app.route("/", methods=("POST", "GET"))
def index():
    form = CreateTaskForm()
    if request.method == "POST":
        if not form.validate_on_submit():
            flash("Data is wrong!!")
            return redirect(url_for("index"))
        
        caption = form.caption.data
        new_tast = Task(caption=caption)

        if not new_tast.checkCaption(caption=caption):
            flash("Caption is not valid!")
            return redirect(url_for("index"))

        try:
            db.session.add(new_tast)
            db.session.commit()
        except:
            flash("Something went wrong during adding your task")
            return redirect(url_for("index"))

    tasks = Task.query.all()
    return render_template("index/index.html", form=form, tasks=tasks)


@app.route("/delete/<int:id>")
def deleteTask(id):
    task = Task.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
    except:
        flash("Something went wrong during deleting your task")
        return redirect(url_for("index"))

    return redirect(url_for("index"))


@app.route("/update/<int:id>", methods=("POST", "GET"))
def updateTask(id):
    task = Task.query.get_or_404(id)

    if request.method == "POST":
        form = request.form.to_dict()
        new_caption = form["caption"]

        if not new_caption:
            flash(f"Something went wrong during updating your task id : {id}")
            return redirect(url_for("updateTask", id=id))

        task.caption = new_caption

        try:
            db.session.commit()
            return redirect("/")
        except:
            flash(f"Something went wrong during updating your task id : {id}")
            return redirect(url_for("updateTask",id=id))

    return render_template("index/update.html", task=task)
