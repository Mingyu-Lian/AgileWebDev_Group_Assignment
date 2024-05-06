import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, current_user
from .forms import LoginForm, SignUpForm,UploadForm
from .models import db, User

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
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Successfully registered!')
        return redirect(url_for('main.login'))
    return render_template('signup.html', title='Sign Up', form=form)

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html', title='Home')

@main.route('/profile')
def profile():
    return render_template('profile.html', title='Profile')

@main.route('/market')
def market():
    return render_template('market.html', title='Home')


@main.route('/upload/product', methods=['GET', 'POST'])
def upload_product():
    form = UploadForm()
    if form.validate_on_submit():
        # 处理文件上传逻辑
        title = form.title.data
        description = form.description.data
        file = form.image.data

        # 保存文件到指定路径，假设保存到静态文件夹中的 uploads 文件夹
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('main.home'))

    return render_template('upload.html', title='Upload Post', form=form)