import os
from flask import Flask
from api.config.config import DevelopmentConfig, ProductionConfig
from api.utils.database import db
from api.routes.video import video_route


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(video_route)

    return app