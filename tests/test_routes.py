import unittest
from app import create_app, db
from app.models import User, Post, Comment, Follow
from flask import url_for

class RouteTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the test environment
        # Create a testing instance of the application
        self.app = create_app('testing')
        # Push the application context
        self.app_context = self.app.app_context()
        self.app_context.push()
        # Initialize the database
        db.create_all()
        # Create a test client
        self.client = self.app.test_client()

    def tearDown(self):
        # Clean up the test environment
        # Remove the database session
        db.session.remove()
        # Drop all database tables
        db.drop_all()
        # Pop the application context
        self.app_context.pop()

    def login(self, username, password):
        # Simulate a user login
        # Send a POST request to the login route with the given username and password
        return self.client.post(
            url_for('main.login'),
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    def test_home_route(self):
        # Test the home route
        # Send a GET request to the home route and check if the response status code is 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_route(self):
        # Test the login route
        # Send a GET request to the login route and check if the response status code is 200
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_signup_route(self):
        # Test the signup route
        # Send a GET request to the signup route and check if the response status code is 200
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_logout_route(self):
        # Test the logout route
        # Create a test user and commit to the database
        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        db.session.add(u1)
        db.session.commit()
        # Simulate a login with the test user
        self.login('john', 'cat')
        # Send a GET request to the logout route with follow_redirects set to True
        response = self.client.get('/logout', follow_redirects=True)
        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

    def test_profile_route(self):
        # Test the profile route
        # Create a test user and commit to the database
        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        db.session.add(u1)
        db.session.commit()
        # Simulate a login with the test user
        self.login('john', 'cat')
        # Send a GET request to the profile route with follow_redirects set to True
        response = self.client.get('/profile', follow_redirects=True)
        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

    def test_upload_product_route(self):
        # Test the upload product route
        # Create a test user and commit to the database
        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        db.session.add(u1)
        db.session.commit()
        # Simulate a login with the test user
        self.login('john', 'cat')
        # Send a GET request to the upload product route
        response = self.client.get('/upload/product')
        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

    def test_show_post_route(self):
        # Test the show post route
        # Create a test user and commit to the database
        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        db.session.add(u1)
        db.session.commit()
        # Create a test post by the test user and commit to the database
        p1 = Post(title='Test Post', description='This is a test post', author=u1)
        db.session.add(p1)
        db.session.commit()
        # Simulate a login with the test user
        self.login('john', 'cat')
        # Send a GET request to the show post route with the post id
        response = self.client.get(f'/post/{p1.id}')
        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

    def test_follow_route(self):
        # Test the follow route
        # Create two test users and commit to the database
        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        u2 = User(username='jane', email='jane@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        # Simulate a login with the first test user
        self.login('john', 'cat')
        # Send a GET request to the follow route with the second user's id and follow_redirects set to True
        response = self.client.get(f'/follow/{u2.id}', follow_redirects=True)
        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)
        # Verify that the first user is following the second user
        self.assertTrue(u1.is_following(u2))

    def test_unfollow_route(self):
        # Test the unfollow route
        # Create two test users and commit to the database
        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        u2 = User(username='jane', email='jane@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        # Create a follow relationship between the two users and commit to the database
        follow = Follow(follower=u1, followed=u2)
        db.session.add(follow)
        db.session.commit()
        # Simulate a login with the first test user
        self.login('john', 'cat')
        # Send a GET request to the unfollow route with the second user's id and follow_redirects set to True
        response = self.client.get(f'/unfollow/{u2.id}', follow_redirects=True)
        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)
        # Verify that the first user is no longer following the second user
        self.assertFalse(u1.is_following(u2))

    def test_user_channel_route(self):
        # Test the user channel route
        # Create a test user and commit to the database
        u1 = User(username='john', email='john@example.com')
        db.session.add(u1)
        db.session.commit()
        # Send a GET request to the user channel route with the username
        response = self.client.get(f'/user/{u1.username}')
        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

    def test_followers_route(self):
        # Test the followers route
        # Create two test users and commit to the database
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='jane', email='jane@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        # Create a follow relationship where the second user follows the first user and commit to the database
        follow = Follow(follower=u2, followed=u1)
        db.session.add(follow)
        db.session.commit()
        # Send a GET request to the followers route with the first user's id
        response = self.client.get(f'/followers/{u1.id}')
        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)
        # Verify that the response contains the second user's username
        self.assertIn(u2.username, response.get_data(as_text=True))

    def test_following_route(self):
        # Test the following route
        # Create two test users and commit to the database
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='jane', email='jane@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        # Create a follow relationship where the first user follows the second user and commit to the database
        follow = Follow(follower=u1, followed=u2)
        db.session.add(follow)
        db.session.commit()
        # Send a GET request to the following route with the first user's id
        response = self.client.get(f'/following/{u1.id}')
        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)
        # Verify that the response contains the second user's username
        self.assertIn(u2.username, response.get_data(as_text=True))

    def test_reset_password_route(self):
        # Test the reset password route
        # Create a test user and commit to the database
        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        db.session.add(u1)
        db.session.commit()
        # Simulate a login with the test user
        self.login('john', 'cat')
        # Send a GET request to the reset password route
        response = self.client.get('/reset_password')
        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

    if __name__ == '__main__':
        unittest.main()