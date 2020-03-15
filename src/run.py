import os
from main import create_app
from api.config.config import ProductionConfig,\
    DevelopmentConfig, TestConfig


if os.environ.get('WORK_ENV') == 'PROD':
    app = create_app(ProductionConfig)
elif os.environ.get('WORK_ENV') == 'TEST':
    app = create_app(TestConfig)
else:
    app = create_app(DevelopmentConfig)


if __name__ == "__main__":
    app.run()
