class Config(object):
    DEBUG = True
    UPLOAD_FOLDER = '/tmp/data'
    FILE_STORAGE_PATH = '/home/Videos/test_videos'
    HOST = '127.0.0.1'
    STATIC_URL = 'static/'
    MAX_CONTENT_LENGTH = 10000 * 1024 * 1024


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
