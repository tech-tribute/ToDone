# Configuration

class Config:
    pass


class Development(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False
