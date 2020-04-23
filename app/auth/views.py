from flask import render_template, request, url_for, flash, redirect
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm
from ..email import send_email


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
        and not current_user.confirmed \
        and request.blueprint != 'auth' \
        and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # 实例化form
    if form.validate_on_submit():  # 如果点击submit
        user = User.query.filter_by(email=form.email.data).first()
        # 查找User.query(关键字段为email符合表格中输入的form.email.data)第一个
        if user is not None and user.verify_password(form.password.data):
        # 如果 用户存在 且 验证用户密码为真
            login_user(user, form.remember_me.data)
            # (根据后面记住我为True or False 是否把用户标记为已登录
            next = request.args.get('next')
            # 把原来URL保存在查询字符串next中
            if next is None or not next.startswith('/'):
            # 如果 next 不存在 或者 next以/开始
                next =url_for('main.index')
                # 重定向到首页
            return redirect (next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)  #  都存在问题重新渲染登录页面


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm() # 实例化form
    if form.validate_on_submit(): # 如果点击提交
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        # 当前用户生成token
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, toekn=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    # 检验当前用户是否已经确认过
    if current_user.confirmed:
        # 确认过则重定向到首页
        return redirect(url_for('main.index'))  # 重定向主页
    # 未确认过则再次进行确认token,如果token有效
    if current_user.confirm(token):
        # 提交到数据库, 创建id
        db.session.commit()
        # 反馈信息
        flash('You have confirmed your account. Thanks!')
    # token无效则返回
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():  # 再次发送确认消息
    token = current_user.generate_confirmation_token()  # 当前用户生成toekn
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)  # 发送email
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))
