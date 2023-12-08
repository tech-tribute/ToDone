from flask import Flask
from todone.config import Development, Production


app = Flask(__name__)

# Configure app
app.config.from_object(Development)