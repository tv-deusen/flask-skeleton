import pytest

from readit.app import auth

from flask import g, session


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    pass



def test_login(client, app):
    pass


