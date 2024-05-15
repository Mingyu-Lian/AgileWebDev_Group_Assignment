import unittest
from app import create_app, db
from app.forms import LoginForm, SignUpForm, ProfileForm, IconForm, UploadForm, CommentForm, ResetPasswordForm

class FormTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_form(self):
        form = LoginForm(username='john', password='cat')
        self.assertTrue(form.validate())

    def test_signup_form(self):
        form = SignUpForm(
            username='john',
            email='john@example.com',
            password='cat',
            confirm_password='cat'
        )
        self.assertTrue(form.validate())

    def test_profile_form(self):
        form = ProfileForm(
            name='John Doe',
            address='123 Main St',
            company='Acme Inc.',
            city='New York',
            country='USA',
            phone='1234567890',
            job_title='Software Engineer',
            job_description='Develop software applications',
            education_level='Bachelor\'s Degree',
            academic_institution='XYZ University'
        )
        self.assertTrue(form.validate())

    def test_icon_form(self):
        # 测试IconForm需要模拟一个文件上传
        pass

    def test_upload_form(self):
        form = UploadForm(
            title='Test Post',
            description='This is a test post',
            tag='1'
        )
        self.assertTrue(form.validate())

    def test_comment_form(self):
        form = CommentForm(content='This is a test comment')
        self.assertTrue(form.validate())

    def test_reset_password_form(self):
        form = ResetPasswordForm(
            password='newpassword',
            confirm_password='newpassword'
        )
        self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main()