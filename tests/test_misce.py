import unittest
from datetime import datetime
from app import create_app, db
from app.models import User, Post, Comment, Category, Follow, UserDetails


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_model_unique_constraints(self):

        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        db.session.add(u1)
        db.session.commit()

        u2 = User(username='john', email='john_doe@example.com')
        u2.set_password('dog')
        db.session.add(u2)
        with self.assertRaises(Exception):
            db.session.commit()
        db.session.rollback()

        u3 = User(username='jane', email='john@example.com')
        u3.set_password('dog')
        db.session.add(u3)
        with self.assertRaises(Exception):
            db.session.commit()
        db.session.rollback()


    def test_cascade_delete(self):

        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        db.session.add(u1)
        db.session.commit()
        c1 = Category(name='Technology')
        db.session.add(c1)
        p1 = Post(title='Test Post', description='This is a test post', author=u1, category=c1)
        db.session.add(p1)
        db.session.commit()
        c2 = Comment(body='This is a test comment', author_id=u1.id, post_id=p1.id)
        db.session.add(c2)
        db.session.commit()

        db.session.delete(u1)
        db.session.commit()
        self.assertIsNone(Post.query.get(p1.id))
        self.assertIsNone(Comment.query.get(c2.id))

    def test_timestamp(self):

        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        db.session.add(u1)
        db.session.commit()
        p1 = Post(title='Test Post', description='This is a test post', author=u1)
        db.session.add(p1)
        db.session.commit()
        self.assertTrue((datetime.utcnow() - p1.timestamp).total_seconds() < 10)

    def test_error_handling(self):

        with self.assertRaises(Exception):
            u1 = User.query.get(-1)
            self.assertIsNone(u1)

        with self.assertRaises(Exception):
            p1 = Post.query.get(-1)
            self.assertIsNone(p1)


if __name__ == '__main__':
    unittest.main()
