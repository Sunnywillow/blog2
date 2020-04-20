from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)  # 添加email字段,使用电子邮件登录
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    @property  # 将方法变成属性的装饰器
    def password(self):  # 如果试图读取password则返回错误
        raise AttributeError('password is not a readable attribute')
q
    @password.setter   # 设置属性
    def password(self, password):  # 生成的哈希密码成为属性
        self.password_hash = generate_password_hash(password)

    @login_manager.user_loader  # 装饰器把这个函数注册给Flask-Login
    def load_user(user_id):
        return User.query.get(int(user_id))

    def verify_password(self, password):  # 检查哈希密码
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username
