# Configuration


# Comman config
class Config:
    # Secret key used to sign session cookies for protection against cookie data tampering
    SECRET_KEY = "T{}|$_|$$0$3CR3T_LOL"

    # UPLOAD_FOLDER is where we will store the uploaded files
    UPLOAD_FOLDER = "db"


# Configs that will be used during Development
class Development(Config):
    DEBUG = True


# Configs that will be used during Production
class Production(Config):
    DEBUG = False
