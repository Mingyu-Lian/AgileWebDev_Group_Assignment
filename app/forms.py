
#This forms.py file is an assignment of CITS5505 unit in the university of Western Australia (2024 S1)
#This is a part of the Group assingment Group

# the forms file for app to rule the database input format


from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField,FileField,SelectField,EmailField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, Optional
from app.models import User

# forms setting for login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# forms setting for sign up
class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
# exception handling:About the username and email: if they have been taken
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already used. Please use a different email address.')


# forms setting for rpfile setting
class ProfileForm(FlaskForm): # Define the user's profile
    name = StringField('Name')
    address = StringField('Address')
    company = StringField('Company')
    city = StringField('City')
    country = StringField('Country')
    phone = StringField('Phone')
    job_title = StringField('Job Title')
    job_description = StringField('Job Description')
    education_level = StringField('Education Level')
    academic_institution = StringField('Academic Institution')
    submit = SubmitField('Set Profile')

# forms setting for icon setting
class IconForm(FlaskForm): # Define the form to upload the icon path
    img = FileField('Choose an icon', validators=[
        FileRequired(),
        # restrict the data type
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Upload')

# forms setting for Uploading Post
class UploadForm(FlaskForm): #Define the form for upload posts, define the fields and validation rules in the form.
    title = StringField('Title', validators=[DataRequired(message='Title is required.'), Length(max=50)]) #Title is required to be present and can't exceed 50 characters.
    description = TextAreaField('Description', validators=[Length(max=500), Optional()]) #Post descriptions are not required and are limited to 500 characters.
    tag = SelectField('Tag', choices=[('', ''),('1', 'Interview'), ('2', 'Recruitment'), ('3', 'Seeking'),('4', 'Experience')], validators=[Optional()]) #There are 4 types of category for posts, and their corresponding values, the default is null。
    image = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files allowed.'), Optional()]) #Guaranteed image type and not required to be uploaded。
    submit = SubmitField('Submit')

# forms setting for Comments
class CommentForm(FlaskForm): #Define the form for comment, define the fields and validation rules in the form.
    content = TextAreaField('Comment', validators=[DataRequired(), Length(max=500)]) # Limit comments to 500 characters and require a date.
    submit = SubmitField('Submit')

# forms setting for Resetting Password
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('reset_password')

    

