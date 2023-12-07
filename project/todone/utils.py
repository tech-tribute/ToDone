from todone import app
import json

import datetime
import time
import random
import os


# list of allowed file formats
ALLOWED_EXTENSIONS = {"json"}
# Address of route directory (TODONE)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Error
class FileNotAllowedError(Exception):
    """The format of file is not allowed"""
    pass


# Check if the format is allowed
def allowedFile(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Getting time (In this program, it is used for the json/db name)
def now():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


# Generate unique id
def generate_numeric_id():
    timestamp = int(time.time() * 1000)  # Convert current time to milliseconds
    random_number = random.randint(1, 1000)  # Generate a random number
    unique_id = int(f"{timestamp}{random_number}")
    return unique_id


# Create a json/db in db folder
def create_json():
    # making path
    filename = f"{now()}.json"
    filepath = os.path.join(ROOT_DIR, f"{app.config['UPLOAD_FOLDER']}\{filename}")

    # create a json file
    with open(filepath, "w") as file:
        json.dump([], file, indent=4)

    return filename


# Path of db folder in user's pc + filename
def generate_json_path(filename):
    return os.path.join(ROOT_DIR, f"{app.config['UPLOAD_FOLDER']}\{filename}")


# Get path by filter
def filter_by(filter_, task_manager):
    if filter_:
        if filter_ == "all":
            tasks = task_manager.query_all()
        elif filter_ == "completed":
            tasks = task_manager.query_done_tasks()
        elif filter_ == "active":
            tasks = task_manager.query_undone_tasks()
    else:
        tasks = task_manager.query_all()

    return tasks
