from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from todone.config import Development
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Development)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from todone import router
