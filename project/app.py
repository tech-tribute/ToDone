from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite.db"
db = SQLAlchemy(app)


class Task(db.Model):
    __tablename__ = "tasks"
    id = Column(Integer(), nullable=False, primary_key=True)
    caption = Column(String(128), nullable=False)
    create = Column(DateTime(), default=datetime.now, nullable=False)


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


if __name__ == "__main__":
    app.run(debug=True, port=8000)
