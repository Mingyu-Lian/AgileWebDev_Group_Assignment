from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user
from .forms import LoginForm, SignUpForm
from .models import db, User, UserDetails

main = Blueprint('main', __name__)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.home'))
    return render_template('login.html', title='Sign In', form=form)

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('The email is already registered')
            return redirect(url_for('main.signup'))
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.flush()

        new_user_details = UserDetails(id=new_user.id)
        db.session.add(new_user_details)

        db.session.commit()
        flash('Successfully registered!')
        return redirect(url_for('main.login'))
    return render_template('signup.html', title='Sign Up', form=form)

@main.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.login'))

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html', title='Home')

@main.route('/profile')
def profile():
    return render_template('profile.html', title='Profile')

@main.route('/upload')
def upload():
    return render_template('upload.html', title='Upload')

@main.route('/post')
def post():
    return render_template('home.html', title='Post')

@main.route('/channel')
def channel():
    return render_template('channel.html', title='Channel')

@main.route('/search')
def search():
    return render_template('search.html', title='Search')
