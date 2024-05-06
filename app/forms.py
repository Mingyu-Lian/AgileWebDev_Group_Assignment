from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField,FileField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from wtforms.fields import EmailField
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
        
class UploadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message='Title is required.'),Length(max=50)])
    description = TextAreaField('Description', validators=[DataRequired(message='Description is required.'),Length(max=500)])
    tag = SelectField('Tag', choices=[('interview', 'Interview'), ('recruitment', 'Recruitment'), ('job_search', 'Job Search')], validators=[DataRequired()])
    image = FileField('Image', validators=[DataRequired(message='Image is required.'),FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField('Submit')