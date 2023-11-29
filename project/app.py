from todone import app


if __name__ == "__main__":
    # during development
    # instead of code above run these codes below in terminal :
    # >>> flask db init
    # >>> flask db migrate
    # >>> flask db upgrade

    app.run(debug=True, port=8000)
