import os

from config import Config
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import Flask, g
from . import auth, models

def __init_logging(app):
    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Skeleton Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/skeleton.log', maxBytes=10240,
                                        backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Skeleton startup')


def create_app(test_config=None):
    """
    Instead of creating a Flask instance globally, you will create it inside a function. 
    This function is known as the application factory. 
    Any configuration, registration, and other setup the application needs will happen
    inside the function, then the application will be returned.
    """

    # a Flask application is an instance of the Flask class
    app = Flask(__name__, instance_relative_config=True)
    # initial default config
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'readit.sqlite')
    )
    
    if test_config is None:
        # Load instance config, if it exists, when not testing
        # overrides the default config with values taken from config.py
        # in the instance folder if it exists
        app.config.from_object(Config)
    else:
        # Load test config if passed in
        app.config.from_object(test_config)

    try:
        # Flask doesn’t create the instance folder automatically,
        # but it needs to be created because your project will
        # create the SQLite database file there
        os.makedirs(app.instance_path)
    except OSError:
        pass

    __init_logging(app)

    app.register_blueprint(auth.bp)

    with app.app_context():    
        g.db = SQLAlchemy(app)

    return app
