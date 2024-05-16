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

    def test_user_model_unique_constraints(self):
        # Test that the user model has unique constraints for username and email

        # Create and add a user to the database
        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        db.session.add(u1)
        db.session.commit()

        # Attempt to create another user with the same username
        u2 = User(username='john', email='john_doe@example.com')
        u2.set_password('dog')
        db.session.add(u2)
        with self.assertRaises(Exception):  # Expecting an integrity error due to unique constraint violation
            db.session.commit()
        db.session.rollback()

        # Attempt to create another user with the same email
        u3 = User(username='jane', email='john@example.com')
        u3.set_password('dog')
        db.session.add(u3)
        with self.assertRaises(Exception):  # Expecting an integrity error due to unique constraint violation
            db.session.commit()
        db.session.rollback()

    def test_cascade_delete(self):
        # Test if deleting a post also deletes its associated comments

        # Create and add a user to the database
        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        db.session.add(u1)
        db.session.commit()

        # Create and add a category to the database
        c1 = Category(name='Technology')
        db.session.add(c1)
        db.session.commit()

        # Create and add a post to the database
        p1 = Post(title='Test Post', description='This is a test post', author=u1, category=c1)
        db.session.add(p1)
        db.session.commit()

        # Create and add a comment to the post
        c2 = Comment(body='This is a test comment', author_id=u1.id, post_id=p1.id)
        db.session.add(c2)
        db.session.commit()

        # Delete the post
        db.session.delete(p1)
        db.session.commit()

        # Verify that the post and its associated comments are deleted
        self.assertIsNone(Post.query.get(p1.id))
        self.assertIsNone(Comment.query.get(c2.id))

    def test_timestamp(self):
        # Test if posts have a timestamp

        # Create and add a user to the database
        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        db.session.add(u1)
        db.session.commit()

        # Create and add a post to the database
        p1 = Post(title='Test Post', description='This is a test post', author=u1)
        db.session.add(p1)
        db.session.commit()

        # Verify that the post's creation timestamp is within the last 10 seconds
        self.assertTrue((datetime.utcnow() - p1.created_at).total_seconds() < 10)

    def test_error_handling(self):
        # Test error handling for querying non-existent users and posts

        with self.assertRaises(Exception):
            u1 = User.query.get(-1)
            self.assertIsNone(u1)

        with self.assertRaises(Exception):
            p1 = Post.query.get(-1)
            self.assertIsNone(p1)


if __name__ == '__main__':
    unittest.main()
