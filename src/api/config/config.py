class Config(object):
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    UPLOAD_FOLDER = '/tmp'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    UPLOAD_FOLDER = '/mnt/data/test_video'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024
