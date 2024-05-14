import unittest
from app import create_app, db
from app.models import User, Post, Comment, Follow
from flask import url_for

class RouteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_route(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_signup_route(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_logout_route(self):
        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        db.session.add(u1)
        db.session.commit()
        with self.client:
            self.client.post(
                url_for('main.login'),
                data=dict(username=u1.username, password='cat'),
                follow_redirects=True
            )
            response = self.client.get('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_profile_route(self):
        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        db.session.add(u1)
        db.session.commit()
        with self.client:
            self.client.post(
                url_for('main.login'),
                data=dict(username=u1.username, password='cat'),
                follow_redirects=True
            )
            response = self.client.get('/profile')
            self.assertEqual(response.status_code, 200)

    def test_upload_product_route(self):
        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        db.session.add(u1)
        db.session.commit()
        with self.client:
            self.client.post(
                url_for('main.login'),
                data=dict(username=u1.username, password='cat'),
                follow_redirects=True
            )
            response = self.client.get('/upload/product')
            self.assertEqual(response.status_code, 200)

    def test_show_post_route(self):
        u1 = User(username='john', email='john@example.com')
        db.session.add(u1)
        db.session.commit()
        p1 = Post(title='Test Post', description='This is a test post', author=u1)
        db.session.add(p1)
        db.session.commit()
        response = self.client.get(f'/post/{p1.id}')
        self.assertEqual(response.status_code, 200)

    def test_follow_route(self):
        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        u2 = User(username='jane', email='jane@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        with self.client:
            self.client.post(
                url_for('main.login'),
                data=dict(username=u1.username, password='cat'),
                follow_redirects=True
            )
            response = self.client.get(f'/follow/{u2.id}', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(u1.is_following(u2))


def test_unfollow_route(self):
    u1 = User(username='john', email='john@example.com')
    u1.set_password('cat')
    u2 = User(username='jane', email='jane@example.com')
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()
    follow = Follow(follower=u1, followed=u2)
    db.session.add(follow)
    db.session.commit()
    with self.client:
        self.client.post(
            url_for('main.login'),
            data=dict(username=u1.username, password='cat'),
            follow_redirects=True
        )
        response = self.client.get(f'/unfollow/{u2.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(u1.is_following(u2))


def test_user_channel_route(self):
    u1 = User(username='john', email='john@example.com')
    db.session.add(u1)
    db.session.commit()
    response = self.client.get(f'/user/{u1.username}')
    self.assertEqual(response.status_code, 200)


def test_followers_route(self):
    u1 = User(username='john', email='john@example.com')
    u2 = User(username='jane', email='jane@example.com')
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()
    follow = Follow(follower=u2, followed=u1)
    db.session.add(follow)
    db.session.commit()
    response = self.client.get(f'/followers/{u1.id}')
    self.assertEqual(response.status_code, 200)
    self.assertIn(u2, response.get_data(as_text=True))


def test_following_route(self):
    u1 = User(username='john', email='john@example.com')
    u2 = User(username='jane', email='jane@example.com')
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()
    follow = Follow(follower=u1, followed=u2)
    db.session.add(follow)
    db.session.commit()
    response = self.client.get(f'/following/{u1.id}')
    self.assertEqual(response.status_code, 200)
    self.assertIn(u2, response.get_data(as_text=True))


def test_reset_password_route(self):
    u1 = User(username='john', email='john@example.com')
    u1.set_password('cat')
    db.session.add(u1)
    db.session.commit()
    with self.client:
        self.client.post(
            url_for('main.login'),
            data=dict(username=u1.username, password='cat'),
            follow_redirects=True
        )
        response = self.client.get('/reset_password')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()