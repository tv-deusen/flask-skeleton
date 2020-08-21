import os
import tempfile
import pytest
from werkzeug.security import generate_password_hash

from readit.app import create_app
from readit.app.models import User, Post
from config import Config

#
# Common fixtures used by tests
#

def add_test_user(db):
    
    u = User(username='test',
            email='test@example.com',
            password_hash=generate_password_hash('test'))
    db.session.add(u)
    db.session.commit()
        


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    test_conf = Config()
    test_conf.SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    app = create_app(test_config=test_conf)
    with app.app_conext():
        # Add test Users and Posts?
        users = add_test_user(g.db)
        # posts = add_test_posts(g.db, users)
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


@pytest.fixture
class AuthActions:
    """
    Most views require a user to be logged in.
    Easiest way to do that in test context is to make a
    POST request to the login view with the client.
    These methods do that.
    """
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )
    
    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    """
    With the auth fixture, you can call auth.login() 
    in a test to log in as the test user, which was 
    inserted as part of the test data in the app fixture.
    """
    return AuthActions(client)
