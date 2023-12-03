# Configuration of the app


# Comman configs
class Config:
    # SQLALCHEMY_DATABASE_URI tells SQLAlchemy what database to connect to
    SQLALCHEMY_DATABASE_URI = "sqlite:///sqlite.db"

    # Secret key used to sign session cookies for protection against cookie data tampering
    SECRET_KEY = "T{}|$_|$$0$3CR3T_LOL"

    # UPLOAD_FOLDER is where we will store the uploaded files
    UPLOAD_FOLDER = "uploads"


# Configs that will be used in Development
class Development(Config):
    DEBUG = True


# Configs that will be used in Production
class Production(Config):
    DEBUG = False
