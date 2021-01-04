import os
import tempfile
import shutil

import pytest

from main import create_app
from api.config.config import TestConfig, ProductionConfig, DevelopmentConfig


ENV_CONFIG = {
    'TEST': TestConfig,
    'PROD': ProductionConfig,
    'DEV': DevelopmentConfig
}

@pytest.fixture
def app():
    work_env = os.environ.get('WORK_ENV')
    app_config = ENV_CONFIG.get(work_env, DevelopmentConfig)
    db_fd, db_path = tempfile.mkstemp()
    app_config.SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path
    app_config.UPLOAD_FOLDER = tempfile.mkdtemp()
    app_config.FILE_STORAGE_PATH = tempfile.mkdtemp()
    app = create_app(app_config)

    yield app

    os.close(db_fd)
    os.unlink(db_path)
    shutil.rmtree(app_config.UPLOAD_FOLDER)
    shutil.rmtree(app_config.FILE_STORAGE_PATH)
