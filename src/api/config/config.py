class Config(object):
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    UPLOAD_FOLDER = '/tmp/test_video'
    MAX_CONTENT_LENGTH = 10000 * 1024 * 1024


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    UPLOAD_FOLDER = '/mnt/data/tmp/'
    VIDEO_STORAGE_PATH = '/mnt/data/test_video'
    IMAGE_STORAGE_PATH = '/mnt/data/test_image'
    BASE_IMAGE_URL = '/images/'
    MAX_CONTENT_LENGTH = 10000 * 1024 * 1024
