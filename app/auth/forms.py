from flask_wtf import FlaskForm  # 从flask_wtf 包中导入 FlaskForm模块
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):  # 注册表单类
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    # email 字段 有效值, 1-64个字节, email格式
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    # 用户名 有效值, 64字节, 首位字母后置位只包含字母,数字,下划线和点, 正则标志0, 错误信息
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    # 密码 有效值 调用EqualTo 匹配第二个密码
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    # 确认密码 有效值
    submit = SubmitField('Register')

    def validate_email(self, field):  # 验证email有效
        if User.query.filter_by(email=field.data).first():
            # 如果用户在表格中填写的数据与数据库中的一致
            raise ValidationError('Email already registered.')
            # 返回错误 邮箱已经被注册

    def validate_username(self, field):  # 验证用户名
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')