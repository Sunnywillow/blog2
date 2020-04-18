import unittest
from app.models import User


class UserModelTestCase(unittest.TestCase):

    def test_password_setter(self):  # 测试密码设置
        u = User(password = 'cat')
        self.assertTrue(u.password_hash is not None)  # 如果存在,断言真

    def test_no_password_getter(self):  # 测试禁止密码直接获取
        u = User(password = 'cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):  # 测试密码验证
        u = User(password = 'cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password = 'cat')
        u2 = User(password = 'dog')
        self.assertTrue(u.password_hash != u2.password_hash)