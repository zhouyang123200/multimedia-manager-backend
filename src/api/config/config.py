class Config(object):
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
