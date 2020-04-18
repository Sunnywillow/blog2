from . import db
from werkzeug.security import generate_password_hash, check_password_hash

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
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    @property  # 将方法变成属性的装饰器
    def password(self):  # 如果试图读取password则返回错误
        raise AttributeError('password is not a readable attribute')

    @password.setter   # 设置属性
    def password(self, password):  # 生成的哈希密码成为属性
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):  # 检查哈希密码
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username
