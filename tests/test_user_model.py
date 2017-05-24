# ~*~ encoding: utf-8 ~*~
import unittest
import time
from app.models import User, AnonymousUser
from app import db, create_app


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def test_password_hash(self):
        password_hash = User.generate_password('wadehadedudenda')
        self.assertTrue(User.check_password(password_hash, 'wadehadedudenda'))

    def test_user_document(self):
        user = User(
            email='test@example.com',
            username='test',
            password_hash=User.generate_password('test')
        )
        user.save()
        test_user = User.objects(username='test')
        self.assertFalse(test_user is None)
