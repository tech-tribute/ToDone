from todone import app, db
from os import path


if __name__ == "__main__":
    # with app.app_context(): 
    #     db.create_all()

    # during development
    # instead of code above run these codes below in terminal :
    # >>> flask db init
    # >>> flask db migrate
    # >>> flask db upgrade
    
    app.run(debug=True, port=800)
