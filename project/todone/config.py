class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///sqlite.db"


class Development(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False
