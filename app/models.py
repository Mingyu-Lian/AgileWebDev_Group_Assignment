#This models.py file is an assignment of CITS5505 unit in the university of Western Australia (2024 S1)
#This is a part of the Group assingment Group

# the models file for app to modeling the database

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
# mapping for followers
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

# mapping for likes
user_likes = db.Table(
    'user_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

# mapping for follow
class Follow(db.Model):
    __tablename__ = 'follow'

    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    follower = db.relationship('User', foreign_keys=[follower_id], backref=db.backref('following', lazy='dynamic'))
    followed = db.relationship('User', foreign_keys=[followed_id], backref=db.backref('followers', lazy='dynamic'))


#mapping for User table with generating the password by hash
class User(UserMixin, db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    details = db.relationship('UserDetails', back_populates='user', uselist=False, cascade='all, delete-orphan')

    def is_following(self, user):
        return self.following.filter_by(followed_id=user.id).first() is not None
    # enhance the safety by generating the hashed password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    # use func to check the password is correct
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# mapping for user details: separated from user for leaving the user table only for signing up.
class UserDetails(db.Model):

    __tablename__ = 'user_details'
    # Basic personal details information
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

# mapping for Post
class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    img = db.Column(db.String(200))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))  #Foreign key association for the author, used to output the author's name in connection with the user database.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id')) #Foreign key association of the category, used to output the name of the category by connecting to the category database
    likes = db.Column(db.Integer, default=0) #The default number of likes per post is 0.

    #Creating a one-to-many relationship to a User, find the name that corresponds to the author id.
    author = db.relationship('User', backref=db.backref('posts', lazy=True))
    #Creates a one-to-many relationship to the Comment. back_populates specifies the reverse relationship.
    comments = db.relationship('Comment', back_populates='post', lazy='dynamic')
    #Define a many-to-many relationship with users to indicate which users have liked the post.
    liked_by_users = db.relationship('User', secondary=user_likes, backref=db.backref('liked_posts', lazy='dynamic'))
    #Creating a one-to-many relationship to Category, find the name of the corresponding category id.
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))

     #Calculating the number of likes
    def count_likes(self):
        return len(self.liked_by_users)

    #Check if a user has liked the post
    def is_liked_by_user(self, user_id):
        return user_id in [user.id for user in self.liked_by_users]

    #Liking of posts by users
    def like_post(self, user_id):
        if not self.is_liked_by_user(user_id):
            user = User.query.get(user_id)
            if user:
                self.liked_by_users.append(user)
                db.session.commit()
                
     #Unliking of posts by users
    def unlike_post(self, user_id):
        if self.is_liked_by_user(user_id):
            user = User.query.get(user_id)
            if user:
                self.liked_by_users.remove(user)
                db.session.commit()

# mapping for Commments
class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))  #Foreign key association for the author, used to output the author's name in connection with the user database.
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))   #Foreign key association for the post, output in the corresponding id post
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    body = db.Column(db.Text)

    #Creates a one-to-many relationship to the Post. back_populates specifies the reverse relationship.
    post = db.relationship('Post', back_populates='comments')
    
# mapping for Catgegory
class Category(db.Model): #Stores the category name, which is used to output the category. Because there is no way to enter data into this database, it needs to be manually entered into the database as 1 Interview, 2 Recruitment, 3 Seeking, and 4 Experience.

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)









