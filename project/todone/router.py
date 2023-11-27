from todone import app, db
from flask import request, render_template, redirect
from todone.models import *
from todone.forms import CreateTaskForm

# URLS :


@app.route("/", methods=("POST", "GET"))
def index():
    form = CreateTaskForm()
    if request.method == "POST":
        if not form.validate_on_submit():
            return "Data is not valid!", 400
        caption = form.caption.data
        new_tast = Task(caption=caption)

        if not new_tast.checkCaption(caption=caption):
            return "Camtion is not valid!", 400
        
        try :
            db.session.add(new_tast)
            db.session.commit()
        except:
            return "Something went wrong during adding your task", 500
        
    
    tasks = Task.query.all()
    return render_template("index/index.html", form=form, tasks=tasks)


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
