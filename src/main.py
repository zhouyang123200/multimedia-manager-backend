import os
from flask import Flask
from api.config.config import DevelopmentConfig, ProductionConfig
from api.utils.database import db
from api.routes.video import video_route


app = Flask(__name__)

if os.environ.get('WORK_ENV') == 'PROD':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(video_route)

if __name__ == "__main__":
    app.run(port=5000)
