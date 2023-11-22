from flask import render_template, request
from configs import app
from models import database
from datetime import datetime

@app.route("/", methods=("POST", "GET"))
def index():
    if request.method == "POST":
        global database
        form=request.form.to_dict()
        caption = form["caption"]
        create = datetime.now()

        assert len(caption) > 10

        task = {"caption":caption, "create": create}
        database["tasks"].append(task)

    tasks = database["tasks"]
    return render_template("index/index.html", tasks=tasks)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
