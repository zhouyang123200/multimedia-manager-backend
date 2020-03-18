import os
import tempfile
import shutil

import pytest

from main import create_app
from api.config.config import TestConfig


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    TestConfig.UPLOAD_FOLDER = tempfile.mkdtemp()
    TestConfig.SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path
    app = create_app(TestConfig)
    client = app.test_client()

    yield app

    os.close(db_fd)
    os.unlink(db_path)
    shutil.rmtree(TestConfig.UPLOAD_FOLDER)
