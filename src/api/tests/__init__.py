import os
import tempfile

import pytest

from main import create_app
from api.config.config import TestConfig


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    TestConfig.SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path
    app = create_app(TestConfig)

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(db_path)
