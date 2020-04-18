from flask import render_template, request, url_for, flash, redirect
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User
from .forms import LoginForm

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
    return render_template('auth/login.html')  #  都存在得定向到登录页面


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))