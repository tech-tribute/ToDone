from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from todone.config import Development
from flask_migrate import Migrate


app = Flask(__name__)

# Configuring the app from an object of Development Class that there is in project/todone/config.py
app.config.from_object(Development)

# Creating database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# We do this so that the urls inside the file is known to the program
from todone import router
