from todone import app
from flask import render_template


# Create your views/routers here.
@app.route("/",)
def index():
    return render_template("index.html")
