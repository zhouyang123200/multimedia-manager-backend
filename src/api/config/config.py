class Config(object):
    DEBUG = True
    UPLOAD_FOLDER = '/tmp/data'
    VIDEO_STORAGE_PATH = '/mnt/data/test_video'
    IMAGE_STORAGE_PATH = '/mnt/data/test_image'
    BASE_IMAGE_URL = '/images/'
    MAX_CONTENT_LENGTH = 10000 * 1024 * 1024


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
