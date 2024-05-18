
#This config.py file is an assignment of CITS5505 unit in the university of Western Australia (2024 S1)
#This is a part of the Group assingment Group

# the config file for app to seeting the configuration

import os

basedir = os.path.abspath(os.path.dirname(__file__))

# general config
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'user_icon', 'uploads')
    UPLOAD_POST_IMG = os.path.join(basedir, 'static', 'post_image')
    DEFAULT_POST_IMAGE_PATH = os.path.join(basedir, 'static', 'post_image', 'default.jpg')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SERVER_NAME = os.environ.get('SERVER_NAME') or '127.0.0.1:5000'
    
    APPLICATION_ROOT = os.environ.get('APPLICATION_ROOT') or '/'
    PREFERRED_URL_SCHEME = os.environ.get('PREFERRED_URL_SCHEME') or 'http'

# divided by dev and test
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    WTF_CSRF_ENABLED = False
