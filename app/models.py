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

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

user_likes = db.Table(
    'user_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

class Follow(db.Model):
    __tablename__ = 'follow'

    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    follower = db.relationship('User', foreign_keys=[follower_id], backref=db.backref('following', lazy='dynamic'))
    followed = db.relationship('User', foreign_keys=[followed_id], backref=db.backref('followers', lazy='dynamic'))



class User(UserMixin, db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(80))

    details = db.relationship('UserDetails', back_populates='user', uselist=False, cascade='all, delete-orphan')

    def is_following(self, user):
        return self.following.filter_by(followed_id=user.id).first() is not None
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserDetails(db.Model):

    __tablename__ = 'user_details'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(80))
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

    author = db.relationship('User', backref=db.backref('posts', lazy=True))
    comments = db.relationship('Comment', back_populates='post', lazy='dynamic')
    # 定义与用户的多对多关系，用来表示哪些用户点赞了这个帖子
    liked_by_users = db.relationship('User', secondary=user_likes, backref=db.backref('liked_posts', lazy='dynamic'))
    
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))

    def count_likes(self):
        return len(self.liked_by_users)

    def is_liked_by_user(self, user_id):
        return user_id in [user.id for user in self.liked_by_users]

    def like_post(self, user_id):
        if not self.is_liked_by_user(user_id):
            user = User.query.get(user_id)
            if user:
                self.liked_by_users.append(user)
                db.session.commit()

    def unlike_post(self, user_id):
        if self.is_liked_by_user(user_id):
            user = User.query.get(user_id)
            if user:
                self.liked_by_users.remove(user)
                db.session.commit()

class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    body = db.Column(db.Text)

    # 在 Comment 类中只使用 back_populates 指回 Post 类的 relationship
    post = db.relationship('Post', back_populates='comments')


class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)









