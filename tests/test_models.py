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

    def test_user_model(self):

        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        db.session.add(u1)
        db.session.commit()
        self.assertTrue(u1.check_password('cat'))
        self.assertFalse(u1.check_password('dog'))


        u2 = User(username='jane', email='jane@example.com')
        u2.set_password('cat')
        db.session.add(u2)
        db.session.commit()
        follow = Follow(follower=u1, followed=u2)
        db.session.add(follow)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertFalse(u2.is_following(u1))

    def test_post_model(self):

        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        db.session.add(u1)
        db.session.commit()
        c1 = Category(name='Technology')
        db.session.add(c1)
        p1 = Post(title='Test Post', description='This is a test post', author=u1, category=c1)
        db.session.add(p1)
        db.session.commit()
        self.assertEqual(p1.author.username, 'john')
        self.assertEqual(p1.category.name, 'Technology')

        u2 = User(username='jane', email='jane@example.com')
        u2.set_password('cat')
        db.session.add(u2)
        db.session.commit()
        p1.liked_by_users.append(u1)
        p1.liked_by_users.append(u2)
        db.session.commit()
        self.assertEqual(p1.count_likes(), 2)
        self.assertTrue(p1.is_liked_by_user(u1.id))
        self.assertTrue(p1.is_liked_by_user(u2.id))

    def test_comment_model(self):

        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        db.session.add(u1)
        db.session.commit()
        p1 = Post(title='Test Post', description='This is a test post', author=u1)
        db.session.add(p1)
        db.session.commit()
        c1 = Comment(body='This is a test comment', author_id=u1.id, post_id=p1.id)
        db.session.add(c1)
        db.session.commit()
        self.assertEqual(c1.author_id, u1.id)
        self.assertEqual(c1.post_id, p1.id)

    def test_user_details_model(self):

        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        db.session.add(u1)
        db.session.flush()
        ud1 = UserDetails(id=u1.id, name='John Doe', address='123 Main St', company='Acme Inc.')
        db.session.add(ud1)
        db.session.commit()
        self.assertEqual(ud1.user.username, 'john')
        self.assertEqual(ud1.name, 'John Doe')
        self.assertEqual(ud1.address, '123 Main St')
        self.assertEqual(ud1.company, 'Acme Inc.')

if __name__ == '__main__':
    unittest.main()
