
#This Routes.py file is an assignment of CITS5505 unit in the university of Western Australia (2024 S1)
#This is a part of the Group assingment Group

# the routes file for app


import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, session
from flask_login import login_user, current_user,logout_user,login_required

from .forms import LoginForm, SignUpForm,UploadForm, IconForm, ProfileForm, CommentForm, ResetPasswordForm
from .models import db, User,UserDetails,Post,Follow, Comment
from sqlalchemy import or_



#Blueprint
main = Blueprint('main', __name__)

#login route
@main.route('/login', methods=['GET', 'POST'])
def login():
    # check if log in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # login value imported
    form = LoginForm()
    # check the log in condition
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

#singup route
@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    # check the log in condition
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash('The email is already registered')
                return redirect(url_for('main.signup'))

            # variable pipelines for passing the information to database
            new_user = User(username=form.username.data, email=form.email.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.flush()

            # create instance in user details as well
            new_user_details = UserDetails(id=new_user.id)
            db.session.add(new_user_details)


            db.session.commit()
            flash('Successfully registered!')
            return redirect(url_for('main.login'))

        except Exception as e:
            # exception handling
            db.session.rollback()
            if 'username' in str(e):
                flash('Username is too long. Please use a shorter username.')
            elif 'password' in str(e):
                flash('Password is too long. Please use a shorter password.')
            else:
                flash('An error occurred during registration. Please try again.')
            return redirect(url_for('main.signup'))

    return render_template('signup.html', title='Sign Up', form=form)

# logout route
@main.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.login'))

#home page route
@main.route('/')
@main.route('/home')
def home():
    #filter for following
    filter_type = request.args.get('filter', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = 8

    if filter_type == 'following' and current_user.is_authenticated:
        followed_ids = [followed.followed_id for followed in current_user.following]
        posts_query = Post.query.filter(Post.author_id.in_(followed_ids))
    else:
        posts_query = Post.query

    #pagination function
    posts_pagination = posts_query.order_by(Post.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    posts = posts_pagination.items
    total_posts = posts_query.count()
    total_pages = posts_pagination.pages
    user_profile = UserDetails.query.filter_by(id=current_user.id).first() if current_user.is_authenticated else None

    return render_template(
        'home.html',
        posts=posts,
        filter=filter_type,
        page=page,
        total_pages=total_pages,
        user_profile=user_profile,
        title='Home'
    )

#Profile route
@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # filter the profile by the current user id
    user_profile = UserDetails.query.filter_by(id=current_user.id).first()
    user = User.query.filter_by(id=current_user.id).first()
    # handling exception (although i dont believe this will be useful)
    if not user_profile:
        flash('User not found and please inform this error to dev.', 'error')
        return redirect(url_for('main.home'))
    return render_template('profile.html', user_profile=user_profile, user=user,
        title='Your Profile')

#Set Profile route
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

    # put the previous data inside the forms for the user-friendly design
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
            # exception handling
            flash('Got problems processing the data, please inform the web dev')
            return redirect(url_for('main.profile'))
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))

    return render_template('set_profile.html', title='Set Your Profile', form=form, user_profile=user_profile)

# Set Icon route
@main.route('/profile/set_icon', methods=['GET', 'POST'])
def set_icon():
    form = IconForm()
    user_profile = UserDetails.query.filter_by(id=current_user.id).first()
    if form.validate_on_submit():
        if user_profile:
            file = form.img.data
            # for safety to use secure filename
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

    return render_template('set_icon.html', title='Set Your Icon', form=form, user_profile=user_profile)

#Uplaod page route
@main.route('/upload/product', methods=['GET', 'POST'])
@login_required
def upload_product():


    user_profile = UserDetails.query.filter_by(id=current_user.id).first()
    form = UploadForm() # Example of creating an UploadForm.

    #If the form data is validated and it is a POST request.
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        tag = form.tag.data
        image_file = form.image.data

        if image_file: 
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(filename)
            image_file.save(os.path.join(current_app.config['UPLOAD_POST_IMG'], file_path))#Save the image in the corresponding path.
        else:
            #If no image is uploaded, the default image path is used.
            file_path = 'default.JPG'
        #Saving to the database.
        new_post = Post(title=title, description=description, author_id=current_user.id, category_id=tag, img=file_path)
        db.session.add(new_post)
        db.session.commit()
        #Successful save to the database will notify and jump back to the home page.
        flash('Post uploaded successfully!', 'success')
        return redirect(url_for('main.home'))

    return render_template('upload.html', title='Upload Post', form=form,  user_profile=user_profile)


#Post Showing route
@main.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):

    post = Post.query.get_or_404(post_id)  #Query the post with the specified post_id and return a 404 error page if it doesn't exist.
    comments = Comment.query.filter_by(post_id=post_id).all()  #All comments for querying a specific post_id
    comment_form = CommentForm()  #Example of creating a CommentForm

    user_profile = None
    #If a user submits a comment form and it passes validation
    if current_user.is_authenticated:
        user_profile = UserDetails.query.filter_by(id=current_user.id).first()

        #Look up author information for each comment.
        if comment_form.validate_on_submit():
            comment_body = comment_form.body.data
            new_comment = Comment(body=comment_body, author_id=current_user.id, post_id=post_id)
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('main.show_post', post_id=post_id)) 

    #Look up author information for each comment.
    for comment in comments:
        comment.author = User.query.get(comment.author_id)

    return render_template('post.html', post=post, comments=comments, comment_form=comment_form, user_profile=user_profile,  title='Post Details',)

#Comments route
@main.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    form = CommentForm() #Example of creating a CommentForm.
    post = Post.query.get_or_404(post_id) 
   
    # If the comment form data is validated and submitted via a POST request.
    if form.validate_on_submit():
        comment_body = form.content.data

        new_comment = Comment(body=comment_body, author_id=current_user.id, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()
        
        #Successful save to the database will notify and jump back to the post page.
        flash('Your comment has been added!', 'success')
        return redirect(url_for('main.show_post', post_id=post_id))

    return redirect(url_for('main.show_post', post_id=post_id))

#Like Function route
@main.route('/like_post/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id) 
    #Check if the current user has already liked the post.
    if current_user in post.liked_by_users:
        #Unliked if already liked.
        post.likes -= 1
        post.liked_by_users.remove(current_user)
    else:
        #Performs a like operation if it has not been liked before.
        post.likes += 1
        post.liked_by_users.append(current_user)
    #Saving to the database.
    db.session.commit()
    return redirect(url_for('main.show_post', post_id=post_id))

#Delete Function Route
@main.route('/posts/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    #Check if the currently logged in user is the author of the post.
    if current_user.id != post.author_id:
        flash('You are not authorized to delete this post.', 'error')
        return redirect(url_for('main.show_post',post_id=post.id))
    
    # Delete all comments related to this post
    comments = Comment.query.filter_by(post_id=post_id).all()
    for comment in comments:
        db.session.delete(comment)
    
    #If it is the author of the post, perform the delete post action.
    db.session.delete(post)
    db.session.commit()

    flash('Post deleted successfully.', 'success')
    return redirect(url_for('main.home'))

#Personal Channel route
@main.route('/channel/<int:user_id>', methods=['GET', 'POST'])
def channel(user_id):
    user = User.query.get_or_404(user_id)
    is_own_channel = (current_user.is_authenticated and current_user.id == user_id)
    user_profile = UserDetails.query.filter_by(id=current_user.id).first() if current_user.is_authenticated else None
    other_user_profile = UserDetails.query.filter_by(id=user_id).first()
    posts = Post.query.filter_by(author_id=user_id).order_by(Post.created_at.desc()).all()  # fetch posts
    return render_template('channel.html', user=user, is_own_channel=is_own_channel, user_profile=user_profile, other_user_profile=other_user_profile, posts=posts, title='Channel')

#Search / Search Result route
@main.route('/search', methods=['GET'])
def search():
    user_profile = None
    if current_user.is_authenticated:
        user_profile = UserDetails.query.filter_by(id=current_user.id).first()

    query = request.args.get('query', '')
    filter_type = request.args.get('filter', 'posts')  # default is post

    if query: #search posts title/concent with specific items
        search = f"%{query}%"
        if filter_type == 'posts':
            results = Post.query.join(User).filter(
                db.or_(
                    Post.title.ilike(search),
                    Post.description.ilike(search),
                )
            ).distinct().all()
        elif filter_type == 'users': #search user
            # search user's name / not username
            results = User.query.join(UserDetails).filter(UserDetails.name.ilike(search)).all()

        return render_template('search_results.html', posts=results if filter_type == 'posts' else None,
                               users=results if filter_type == 'users' else None, query=query, filter=filter_type, user_profile=user_profile, title='Search',)
    else:
        flash("Please enter a search term.")
        return redirect(url_for('main.home'))


#Following route
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

#Unfollow route
@main.route('/unfollow/<int:user_id>', methods=['GET', 'POST'])
@login_required
def unfollow(user_id):
    user_to_unfollow = User.query.get_or_404(user_id)

    # to check if following or not
    if current_user.is_following(user_to_unfollow):
    
        current_user.following.filter_by(followed_id=user_id).delete()
        db.session.commit()
        flash(f'You have unfollowed successfully', 'success')
    else:
        
        flash(f'You are not following this user', 'warning')

    
    return redirect(url_for('main.channel', user_id=user_id))

#Follower route
@main.route('/followers/<int:user_id>')
def followers(user_id):
    user_profile = None
    if current_user.is_authenticated:
        user_profile = UserDetails.query.filter_by(id=current_user.id).first()

    user = User.query.get_or_404(user_id)  # make sure user exist
    # get follower's list
    followers = User.query.join(Follow, Follow.follower_id == User.id).filter(Follow.followed_id == user_id).all()
    return render_template('followers.html', user=user, followers=followers, user_profile=user_profile,
                           title='Your Followers')

#Following route
@main.route('/following/<int:user_id>')
def following(user_id):
    user_profile = None
    if current_user.is_authenticated:
        user_profile = UserDetails.query.filter_by(id=current_user.id).first()

    user = User.query.get_or_404(user_id)  # make sure user exist
    # get following's list
    following = User.query.join(Follow, Follow.followed_id == User.id).filter(Follow.follower_id == user_id).all()
    return render_template('following.html', user=user, following=following, user_profile=user_profile,
                           title='Your Following')

# Reset password route
@main.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    user_profile = UserDetails.query.filter_by(id=current_user.id).first()
    if form.validate_on_submit():
        current_user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('main.profile'))
    return render_template('reset_password.html', form=form, user_profile=user_profile,title='Reset Your Password')

#Aboutus page route
@main.route('/aboutus')
def aboutus():
    user_profile = None
    if current_user.is_authenticated:
        user_profile = UserDetails.query.filter_by(id=current_user.id).first()
    return render_template('aboutus.html', user_profile=user_profile,title='About Us')
