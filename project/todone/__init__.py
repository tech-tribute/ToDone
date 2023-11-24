from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from todone.config import Config, Development

app = Flask(__name__)
app.config.from_object(Development)
db = SQLAlchemy(app)

from todone import router
