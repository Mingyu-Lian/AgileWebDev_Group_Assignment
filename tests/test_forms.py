import unittest
from app import create_app, db
from app.forms import LoginForm, SignUpForm, ProfileForm, UploadForm, CommentForm, ResetPasswordForm

class FormTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the test environment
        # Create a testing instance of the application
        self.app = create_app('testing')
        # Push the application context
        self.app_context = self.app.app_context()
        self.app_context.push()
        # Initialize the database
        db.create_all()

    def tearDown(self):
        # Clean up the test environment
        # Remove the database session
        db.session.remove()
        # Drop all database tables
        db.drop_all()
        # Pop the application context
        self.app_context.pop()

    def test_login_form(self):
        # Test the login form validation
        # Create a login form with valid data
        form = LoginForm(username='john', password='cat')
        # Check if the form validates correctly
        self.assertTrue(form.validate())

    def test_signup_form(self):
        # Test the signup form validation
        # Create a signup form with valid data
        form = SignUpForm(
            username='john',
            email='john@example.com',
            password='cat',
            confirm_password='cat'
        )
        # Check if the form validates correctly
        self.assertTrue(form.validate())

    def test_profile_form(self):
        # Test the profile form validation
        # Create a profile form with valid data
        form = ProfileForm(
            name='John Doe',
            address='123 Main St',
            company='Acme Inc.',
            city='New York',
            country='USA',
            phone='1234567890',
            job_title='Software Engineer',
            job_description='Develop software applications',
            education_level="Bachelor's Degree",
            academic_institution='XYZ University'
        )
        # Check if the form validates correctly
        self.assertTrue(form.validate())

    def test_upload_form(self):
        # Test the upload form validation
        # Create an upload form with valid data
        form = UploadForm(
            title='Test Post',
            description='This is a test post',
            tag='1'
        )
        # Check if the form validates correctly
        self.assertTrue(form.validate())

    def test_comment_form(self):
        # Test the comment form validation
        # Create a comment form with valid data
        form = CommentForm(content='This is a test comment')
        # Check if the form validates correctly
        self.assertTrue(form.validate())

    def test_reset_password_form(self):
        # Test the reset password form validation
        # Create a reset password form with valid data
        form = ResetPasswordForm(
            password='newpassword',
            confirm_password='newpassword'
        )
        # Check if the form validates correctly
        self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main()
