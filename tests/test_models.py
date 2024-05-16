import unittest
from datetime import datetime
from app import create_app, db
from app.models import User, Post, Comment, Category, Follow, UserDetails

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        # Create an application instance with the testing configuration
        self.app = create_app('testing')
        # Establish an application context
        self.app_context = self.app.app_context()
        self.app_context.push()
        # Create all database tables
        db.create_all()

    def tearDown(self):
        # Remove the session and drop all tables after each test
        db.session.remove()
        db.drop_all()
        # Pop the application context
        self.app_context.pop()

    def test_user_model(self):
        # Test user model functionality

        # Create and add a user to the database
        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        db.session.add(u1)
        db.session.commit()
        # Check if the password was set correctly
        self.assertTrue(u1.check_password('cat'))
        self.assertFalse(u1.check_password('dog'))

        # Create and add another user to the database
        u2 = User(username='jane', email='jane@example.com')
        u2.set_password('cat')
        db.session.add(u2)
        db.session.commit()
        # Create a follow relationship between the two users
        follow = Follow(follower=u1, followed=u2)
        db.session.add(follow)
        db.session.commit()
        # Verify the follow relationship
        self.assertTrue(u1.is_following(u2))
        self.assertFalse(u2.is_following(u1))

    def test_post_model(self):
        # Test post model functionality

        # Create and add a user to the database
        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        db.session.add(u1)
        db.session.commit()
        # Create and add a category to the database
        c1 = Category(name='Technology')
        db.session.add(c1)
        # Create and add a post to the database
        p1 = Post(title='Test Post', description='This is a test post', author=u1, category=c1)
        db.session.add(p1)
        db.session.commit()
        # Verify the post's author and category
        self.assertEqual(p1.author.username, 'john')
        self.assertEqual(p1.category.name, 'Technology')

        # Create and add another user to the database
        u2 = User(username='jane', email='jane@example.com')
        u2.set_password('cat')
        db.session.add(u2)
        db.session.commit()
        # Add likes to the post
        p1.liked_by_users.append(u1)
        p1.liked_by_users.append(u2)
        db.session.commit()
        # Verify the like count and if the users liked the post
        self.assertEqual(p1.count_likes(), 2)
        self.assertTrue(p1.is_liked_by_user(u1.id))
        self.assertTrue(p1.is_liked_by_user(u2.id))

    def test_comment_model(self):
        # Test comment model functionality

        # Create and add a user to the database
        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        db.session.add(u1)
        db.session.commit()
        # Create and add a post to the database
        p1 = Post(title='Test Post', description='This is a test post', author=u1)
        db.session.add(p1)
        db.session.commit()
        # Create and add a comment to the database
        c1 = Comment(body='This is a test comment', author_id=u1.id, post_id=p1.id)
        db.session.add(c1)
        db.session.commit()
        # Verify the comment's author and post
        self.assertEqual(c1.author_id, u1.id)
        self.assertEqual(c1.post_id, p1.id)

    def test_user_details_model(self):
        # Test user details model functionality

        # Create and add a user to the database
        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        db.session.add(u1)
        db.session.flush()
        # Create and add user details to the database
        ud1 = UserDetails(id=u1.id, name='John Doe', address='123 Main St', company='Acme Inc.')
        db.session.add(ud1)
        db.session.commit()
        # Verify the user details
        self.assertEqual(ud1.user.username, 'john')
        self.assertEqual(ud1.name, 'John Doe')
        self.assertEqual(ud1.address, '123 Main St')
        self.assertEqual(ud1.company, 'Acme Inc.')

if __name__ == '__main__':
    unittest.main()
