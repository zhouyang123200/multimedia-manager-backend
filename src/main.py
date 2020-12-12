import os
import pathlib
from flask import Flask
from api.config.config import DevelopmentConfig, ProductionConfig
from api.utils.database import db
from api.routes.video import video_route


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)
    init_db(app)
    create_all_dir(app)
    register_blueprint(app)

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

def create_all_dir(app):
    pathlib.Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
    pathlib.Path(app.config['FILE_STORAGE_PATH']).mkdir(exist_ok=True)

