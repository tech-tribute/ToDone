class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///sqlite.db"
    SECRET_KEY = "T{}|$_|$$0$3CR3T_LOL"


class Development(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False
