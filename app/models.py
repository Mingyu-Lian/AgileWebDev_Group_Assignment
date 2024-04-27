import os
import uuid

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime


# This grabs our directory
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# Connects our Flask App to our Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self):
        self.id = uuid.uuid4()
        self.username = self.email
        self.email = None


class UserDetails(db.Model):

    __tablename__ = 'user_details'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    address = db.Column(db.Text)
    account = db.Column(db.Float)
    products = db.relationship('Product', backref='seller', lazy=True)
    transactions = db.relationship('Transaction', backref='buyer', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id


class Product(db.Model):

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    img = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.title

    def __init__(self, title, description, img, price, seller_id, category_id):
        self.title = title
        self.description = description
        self.img = img
        self.price = price
        self.seller_id = seller_id
        self.category_id = category_id
        self.seller = UserDetails()


class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name

    def __init__(self, name):
        self.name = name


class Transaction(db.Model):

    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    transaction_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Transaction %r>' % self.id

    def __init__(self, product_id, buyer_id, quantity, total, transaction_time):
        self.product_id = product_id
        self.buyer_id = buyer_id
        self.quantity = quantity
        self.total = total
        self.transaction_time = transaction_time


