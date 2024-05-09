from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField,FileField,SelectField,EmailField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, Optional
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already used. Please use a different email address.')



class ProfileForm(FlaskForm):
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

class IconForm(FlaskForm):
    img = FileField('Choose an icon', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Upload')

class UploadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message='Title is required.'), Length(max=50)])
    description = TextAreaField('Description', validators=[Length(max=500), Optional()])
    tag = SelectField('Tag', choices=[('', ''),('1', 'Interview'), ('2', 'Recruitment'), ('3', 'Job Search')], validators=[Optional()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files allowed.'), Optional()])
    submit = SubmitField('Submit')


    

