from todone import app
import os

if __name__ == "__main__":
    # during development
    # instead of code above run these codes below in terminal :
    # >>> flask db init
    # >>> flask db migrate
    # >>> flask db upgrade

    # Make sure that db folder is created
    os.makedirs(os.path.join("project\\", app.config["UPLOAD_FOLDER"]), exist_ok=True)

    # Run app on port 8000 : http://127.0.0.1:8000
    # Configs are already setted (Check project/todone/config.py and project/todone/__init__.py)
    app.run(port=8000)
