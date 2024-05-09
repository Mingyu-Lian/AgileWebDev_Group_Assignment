import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'user_icon', 'uploads')
    UPLOAD_POST_IMG = os.path.join(basedir, 'static', 'post_image')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
