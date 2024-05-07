import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash



# This grabs our directory
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# Connects our Flask App to our Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user_details.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('user_details.id'), primary_key=True)
)


class User(UserMixin, db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(80))

    details = db.relationship('UserDetails', back_populates='user', uselist=False, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserDetails(db.Model):

    __tablename__ = 'user_details'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    address = db.Column(db.Text)
    img = db.Column(db.String(200))
    company = db.Column(db.String(100))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    phone = db.Column(db.Integer)
    job_title = db.Column(db.String(100))
    job_description = db.Column(db.Text)
    education_level = db.Column(db.String(100))
    academic_institution = db.Column(db.String(100))


    user = db.relationship('User', back_populates='details')

    followed = db.relationship(
        'UserDetails', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    img = db.Column(db.String(200))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    likes = db.Column(db.Integer, default=0)
    following = db.Column(db.Integer, default=0)

    # 在 Post 类中定义 relationship 和 backref
    comments = db.relationship('Comment', back_populates='post', lazy='dynamic')

class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    body = db.Column(db.Text)
    likes = db.Column(db.Integer, default=0)

    # 在 Comment 类中只使用 back_populates 指回 Post 类的 relationship
    post = db.relationship('Post', back_populates='comments')


class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)









