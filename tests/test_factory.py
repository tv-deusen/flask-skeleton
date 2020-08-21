from readit.app import create_app
from config import Config

def test_config():
    assert not create_app().testing
    c = Config()
    c.TESTING = True
    assert create_app(test_config=c).testing
    