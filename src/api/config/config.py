class Config(object):
    DEBUG = True
    UPLOAD_FOLDER = '/tmp/data'
    HOST = '127.0.0.1'
    STATIC_URL = 'static/'
    MAX_CONTENT_LENGTH = 10000 * 1024 * 1024


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    FILE_STORAGE_PATH = '/mnt/mediadata'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    FILE_STORAGE_PATH = '/home/zhouyang/mediadata'


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    FILE_STORAGE_PATH = '/mnt/mediadata'
