

import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, session
from flask_login import login_user, current_user,logout_user,login_required

from .forms import LoginForm, SignUpForm,UploadForm, IconForm, ProfileForm, CommentForm, ResetPasswordForm
from .models import db, User,UserDetails,Post,Follow, Comment
from sqlalchemy import or_





main = Blueprint('main', __name__)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            # Redirect to the intended URL or to the home page
            next_page = session.pop('next', None) or url_for('main.home')
            return redirect(next_page)
        else:
            flash('Invalid username or password')
    # Store the next URL from the query parameters or default to home
    session['next'] = request.args.get('next', url_for('main.home'))
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
    filter_type = request.args.get('filter', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = 8

    if filter_type == 'following' and current_user.is_authenticated:
        followed_ids = [followed.followed_id for followed in current_user.following]
        posts_query = Post.query.filter(Post.author_id.in_(followed_ids))
    else:
        posts_query = Post.query

    posts_pagination = posts_query.order_by(Post.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    posts = posts_pagination.items
    total_posts = posts_query.count()
    total_pages = posts_pagination.pages
    user_profile = UserDetails.query.filter_by(id=current_user.id).first()

    return render_template(
        'home.html',
        posts=posts,
        filter=filter_type,
        page=page,
        total_pages=total_pages,
        user_profile=user_profile
    )






@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_profile = UserDetails.query.filter_by(id=current_user.id).first()    
    if not user_profile:
        flash('User not found and please inform this error to dev.', 'error')
        return redirect(url_for('main.home'))
    return render_template('profile.html', user_profile=user_profile)

@main.route('/profile/set_profile', methods=['GET', 'POST'])
def set_profile():
    form = ProfileForm()
    user_profile = UserDetails.query.filter_by(id=current_user.id).first()

    # Pre-populate the form with existing data when the form is loaded, not submitted
    if request.method == 'GET' and user_profile:
        form.name.data = user_profile.name
        form.address.data = user_profile.address
        form.company.data = user_profile.company
        form.city.data = user_profile.city
        form.country.data = user_profile.country
        form.phone.data = user_profile.phone
        form.job_title.data = user_profile.job_title
        form.job_description.data = user_profile.job_description
        form.education_level.data = user_profile.education_level
        form.academic_institution.data = user_profile.academic_institution

    if form.validate_on_submit():
        if user_profile:
            user_profile.name = form.name.data
            user_profile.address = form.address.data
            user_profile.company = form.company.data
            user_profile.city = form.city.data
            user_profile.country = form.country.data
            user_profile.phone = form.phone.data
            user_profile.job_title = form.job_title.data
            user_profile.job_description = form.job_description.data
            user_profile.education_level = form.education_level.data
            user_profile.academic_institution = form.academic_institution.data
        else:
            flash('Got problems processing the data, please inform the web dev')
            return redirect(url_for('main.profile'))
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))

    return render_template('set_profile.html', title='Profile', form=form, user_profile=user_profile)

@main.route('/profile/set_icon', methods=['GET', 'POST'])
def set_icon():
    form = IconForm()
    user_profile = UserDetails.query.filter_by(id=current_user.id).first()
    if form.validate_on_submit():
        if user_profile:
            file = form.img.data
            filename = secure_filename(file.filename)
            file_path = os.path.join(filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file_path))
            user_profile.img = file_path
            db.session.commit()
            flash('Icon updated successfully!', 'success')
            return redirect(url_for('main.profile'))
        else:
            flash('User profile not found.', 'error')
            return redirect(url_for('main.profile'))

    return render_template('set_icon.html', title='Profile', form=form, user_profile=user_profile)


@main.route('/upload/product', methods=['GET', 'POST'])
@login_required
def upload_product():
    user_profile = UserDetails.query.filter_by(id=current_user.id).first()
    form = UploadForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        tag = form.tag.data
        image_file = form.image.data

        if image_file:
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(filename)
            image_file.save(os.path.join(current_app.config['UPLOAD_POST_IMG'], file_path))
        else:
            # 如果没有上传图片，则使用默认图片路径
            file_path = 'default.JPG'

        new_post = Post(title=title, description=description, author_id=current_user.id, category_id=tag, img=file_path)
        db.session.add(new_post)
        db.session.commit()

        flash('Post uploaded successfully!', 'success')
        return redirect(url_for('main.home'))

    return render_template('upload.html', title='Upload Post', form=form,  user_profile=user_profile)



@main.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        comment_body = comment_form.body.data
        new_comment = Comment(body=comment_body, author_id=current_user.id, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()

    # 查询每条评论的作者信息
    for comment in comments:
        comment.author = User.query.get(comment.author_id)

    return render_template('post.html', post=post, comments=comments, comment_form=comment_form)


@main.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)

    if form.validate_on_submit():
        comment_body = form.content.data

        new_comment = Comment(body=comment_body, author_id=current_user.id, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()

        flash('Your comment has been added!', 'success')
        return redirect(url_for('main.show_post', post_id=post_id))

    # If the form did not validate, redirect back to the post page
    return redirect(url_for('main.show_post', post_id=post_id))

@main.route('/like_post/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if current_user in post.liked_by_users:
        post.likes -= 1
        post.liked_by_users.remove(current_user)
    else:
        post.likes += 1
        post.liked_by_users.append(current_user)
    
    db.session.commit()
    return redirect(url_for('main.show_post', post_id=post_id))


@main.route('/posts/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # 检查当前登录用户是否是帖子的作者
    if current_user.id != post.author_id:
        flash('You are not authorized to delete this post.', 'error')
        return redirect(url_for('main.show_post'))
    
    # 删除帖子
    db.session.delete(post)
    db.session.commit()

    flash('Post deleted successfully.', 'success')
    return redirect(url_for('main.home'))
@main.route('/channel/<int:user_id>', methods=['GET', 'POST'])
def channel(user_id):
    user = User.query.get_or_404(user_id)
    is_own_channel = (current_user.is_authenticated and current_user.id == user_id)
    user_profile = UserDetails.query.filter_by(id=user_id).first()
    posts = Post.query.filter_by(author_id=user_id).order_by(Post.created_at.desc()).all()  # 获取该用户的所有帖子
    return render_template('channel.html', user=user, is_own_channel=is_own_channel, user_id=user_id, user_profile=user_profile, posts=posts)


@main.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    filter_type = request.args.get('filter', 'posts')  # default is post

    if query:
        search = f"%{query}%"
        if filter_type == 'posts':
            results = Post.query.join(User).filter(
                db.or_(
                    Post.title.ilike(search),
                    Post.description.ilike(search),
                )
            ).distinct().all()
        elif filter_type == 'users':
            # 正确地连接 User 和 UserDetails，并通过 UserDetails.name 进行搜索
            results = User.query.join(UserDetails).filter(UserDetails.name.ilike(search)).all()

        return render_template('search_results.html', posts=results if filter_type == 'posts' else None,
                               users=results if filter_type == 'users' else None, query=query, filter=filter_type)
    else:
        flash("Please enter a search term.")
        return redirect(url_for('main.home'))

@main.route('/follow/<int:user_id>', methods=['GET', 'POST'])
@login_required
def follow(user_id):
    user_to_follow = User.query.get_or_404(user_id)
    if current_user == user_to_follow:
        flash('You cannot follow yourself!', 'warning')
        return redirect(url_for('profile', user_id=user_id))

    if current_user.is_following(user_to_follow):
        flash('You are already following this user!', 'warning')
        return redirect(url_for('profile', user_id=user_id))

    follow = Follow(follower_id=current_user.id, followed_id=user_to_follow.id)
    db.session.add(follow)
    db.session.commit()
    flash(f'You are now following the user', 'success')
    return redirect(url_for('main.channel', user_id=user_id))

@main.route('/unfollow/<int:user_id>', methods=['GET', 'POST'])
@login_required
def unfollow(user_id):
    user_to_unfollow = User.query.get_or_404(user_id)

    # to check if following or not
    if current_user.is_following(user_to_unfollow):
    
        current_user.following.filter_by(followed_id=user_id).delete()
        db.session.commit()
        flash(f'You have unfollowed sucessfully', 'success')
    else:
        
        flash(f'You are not following this user', 'warning')

    
    return redirect(url_for('main.channel', user_id=user_id))

@main.route('/user/<username>')
def user_channel(username):
    # 根据用户名获取用户信息
    user = User.query.filter_by(username=username).first()

    if user:
        # 显示用户的 channel 页面
        return render_template('user_channel.html', user=user)
    else:
        # 如果未找到用户，则显示 404 页面或者其他提示
        return render_template('404.html'), 404

@main.route('/followers/<int:user_id>')
def followers(user_id):
    user = User.query.get_or_404(user_id)  # 确保用户存在
    # 获取所有关注当前用户的用户列表
    followers = User.query.join(Follow, Follow.follower_id == User.id).filter(Follow.followed_id == user_id).all()
    return render_template('followers.html', user=user, followers=followers)

@main.route('/following/<int:user_id>')
def following(user_id):
    user = User.query.get_or_404(user_id)  # 确保用户存在
    # 获取当前用户关注的所有用户
    following = User.query.join(Follow, Follow.followed_id == User.id).filter(Follow.follower_id == user_id).all()
    return render_template('following.html', user=user, following=following)


@main.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('main.profile'))
    return render_template('reset_password.html', form=form)