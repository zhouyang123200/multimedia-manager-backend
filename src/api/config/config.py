class Config(object):
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    UPLOAD_FOLDER = '/tmp'
    MAX_CONTENT_LENGTH = 10 * 100 * 1024 * 1024


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    UPLOAD_FOLDER = '/tmp'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024 * 1024
