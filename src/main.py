"""
define flask main app factory function, and do all kinds of setup related app
"""
import os
import pathlib
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_mail import Mail
from werkzeug.routing import BaseConverter
from api.utils.database import db
from api.utils.passwd import jwt
from api.utils.tasks import celery
from api.utils.limiter import limiter
from api.routes.video import video_route
from api.routes.user import user_route, black_list


def create_app(config):
    """
    app factory
    """
    app = Flask(__name__)

    app.config.from_object(config)
    init_db(app)
    jwt_setup(app)
    create_all_dir(app)
    create_regex(app)
    register_blueprint(app)
    setup_log(app)
    mail_setup(app)
    celery_setup(app)
    setup_api_limiter(app)

    return app

def init_db(app):
    """
    init db and create all tables
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()

def register_blueprint(app):
    """
    register all blueprint
    """
    app.register_blueprint(video_route)
    app.register_blueprint(user_route)

def create_all_dir(app):
    """
    create all direactory in init step
    """
    pathlib.Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
    pathlib.Path(app.config['FILE_STORAGE_PATH']).mkdir(exist_ok=True)
    user_file_path = os.path.join(app.config['FILE_STORAGE_PATH'], 'users')
    assets_file_path = os.path.join(app.config['FILE_STORAGE_PATH'], 'assets')
    pathlib.Path(user_file_path).mkdir(exist_ok=True)
    pathlib.Path(assets_file_path).mkdir(exist_ok=True)


def setup_log(app):
    """
    setup log configure
    """
    handler = RotatingFileHandler(app.config['LOG_FILE'], maxBytes=10000, backupCount=1)
    handler.setLevel(app.config['LOG_LEVEL'])
    handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))
    app.logger.addHandler(handler)

def jwt_setup(app):
    """
    setup jwt configure
    """
    jwt.init_app(app)
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in black_list

def mail_setup(app):
    """
    init flask mail
    """
    mail = Mail()
    mail.init_app(app)
    app.mail = mail

def create_regex(app):
    """
    let flask url support regex
    """
    class RegexConverter(BaseConverter):
        """
        regex converter class
        """
        def __init__(self, map, *args):
            self.map = map
            self.regex = args[0]

    app.url_map.converters['regex'] = RegexConverter

def make_celery(app):
    """
    celery app factory
    """
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """
        celery context task class, make every celery task with same flask app
        """
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

def celery_setup(flask_app):
    """
    init celery app
    """
    celery_app = make_celery(flask_app)
    celery_app.finalize()
    flask_app.celery = celery_app

def setup_api_limiter(app):
    """
    user flask limiter to limit api access rate
    """
    limiter.init_app(app)
