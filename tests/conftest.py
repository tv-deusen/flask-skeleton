import os
import tempfile
import pytest


from readit.app import create_app
from config import Config


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'DATABASE': f"sqlite:///{db_path}"
    })
    with app.app_conext():
        #init db
        pass

    yield app
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    test_conf = Config()
    test_conf.SQLALCHEMY_DATABASE_URI = f"'sqlite:///{db_path}"
    
    with readit.app.test_client() as client:
        yield client
    os.close(db_fd)
    os.unlink(test_conf.SQLALCHEMY_DATABASE_URI)

