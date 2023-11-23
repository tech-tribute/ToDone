from app import app, db
from flask import request, render_template, redirect
from todone.models import *


# URLS :

@app.route("/", methods=("POST", "GET"))
def index():
    if request.method == "POST":
        form = request.form.to_dict()
        caption = form["caption"]

        # validation
        if not caption:
            return "You must enter something for caption!"

        try:
            new_task = Task(caption=caption)
            db.session.add(new_task)
            db.session.commit()
        except:
            return "something went wrong! (During adding your task)"

        return redirect("/")
    elif request.method == "GET":
        tasks = Task.query.all()

    return render_template("index/index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def deleteTask(id):
    task = Task.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
    except:
        return f"Something went wrong during deleting the task id:{id}"

    return redirect("/")


@app.route("/update/<int:id>", methods=("POST", "GET"))
def updateTask(id):
    task = Task.query.get_or_404(id)

    if request.method == "POST":
        form = request.form.to_dict()
        new_caption = form["caption"]

        if not new_caption:
            return "You must enter something for caption!"

        task.caption = new_caption

        try:
            db.session.commit()
            return redirect("/")
        except:
            return f"Something went wrong during updating the task id:{id}"

    return render_template("index/update.html", task=task)
