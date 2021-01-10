import os
import pathlib
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from api.config.config import DevelopmentConfig, ProductionConfig
from api.utils.database import db
from api.utils.passwd import jwt
from api.routes.video import video_route
from api.routes.user import user_route, black_list


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)
    init_db(app)
    jwt_setup(app)
    create_all_dir(app)
    register_blueprint(app)
    setup_log(app)

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
