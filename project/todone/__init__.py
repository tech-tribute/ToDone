from flask import Flask
from todone.config import Development, Production


app = Flask(__name__)

# Configure the app from an object of Development Class >>> project/todone/config.py
app.config.from_object(Development)

# To identify routers
from todone import router
