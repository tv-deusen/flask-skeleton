import os
import tempfile
import pytest
import pdb

import readit
from config import Config

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    test_conf = Config()
    test_conf.SQLALCHEMY_DATABASE_URI = f"'sqlite:///{db_path}"
    
    with readit.app.test_client() as client:
        yield client
    os.close(db_fd)
    os.unlink(test_conf.SQLALCHEMY_DATABASE_URI)

