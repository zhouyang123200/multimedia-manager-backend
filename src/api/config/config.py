import logging

class Config(object):
    DEBUG = True
    UPLOAD_FOLDER = '/tmp/data'
    HOST = '127.0.0.1'
    STATIC_URL = 'static/'
    MAX_CONTENT_LENGTH = 10000 * 1024 * 1024
    SECRET_KEY = 'akAjTCGc2CRHU12R6z+eekbk8wPs3tKL'
    JWT_ERROR_MESSAGE_KEY = 'message'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    LOG_FILE = '/home/zhouyang/log/app.log'
    LOG_LEVEL = logging.INFO


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    FILE_STORAGE_PATH = '/mnt/mediadata'
    LOG_FILE = '/var/log/app.log'
    LOG_LEVEL = logging.INFO


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    FILE_STORAGE_PATH = '/mnt/mediadata'
    MAIL_SERVER = ''
    MAIL_PORT = 25 
    MAIL_USERNAME = ''
    MAIL_PASSWORD = '' 
    MAIL_SUPPRESS_SEND = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    FILE_STORAGE_PATH = '/mnt/mediadata'
    LOG_FILE = '/var/log/multimedia/app.log'
    LOG_LEVEL = logging.INFO
