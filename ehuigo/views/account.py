# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Blueprint, redirect, request, url_for, render_template, session, flash, g
from flask.ext.login import login_user, logout_user, login_required, current_user

from ..models import User
from ..forms import RegisterForm
from ..extensions import db
from ..helpers import send_email
from ..constants import USER_STATUS


account = Blueprint('account', __name__, url_prefix='/account')


@account.route('/login/', methods=['GET', 'POST'])
def login():
    # 已登录用户则返回首页
    if current_user.is_authenticated():
        return redirect(request.args.get('next') or url_for('admin.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(email=username).first()
        # print user
        next_ = session.pop('next', None)
        if user and user.verify_password(password):
            login_user(user)
            return redirect(next_ or url_for('admin.index'))
        else:
            flash('用户名或密码错误', 'danger')
            return redirect(url_for('account.login', next=next_))
    session['next'] = request.args.get('next')
    return render_template('account/login.html')


@account.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))


@account.route('/register/', methods=['GET', 'POST'])
def register():
    # 已登录用户则返回首页
    if current_user.is_authenticated():
        return redirect(url_for('admin.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_activation_token()
        send_email(user.email, '账户激活', 'mail/activation.html', user=user, token=token)
        flash('注册成功，您的邮箱 {email} 将会收到一封激活邮件，请在一小时内查收邮件进行账户激活'.format(email=user.email), 'success')
        return redirect(url_for('account.login'))
    return render_template('account/register.html', form=form)


@account.route('/activation/resend/')
@login_required
def resend_activation():
    token = current_user.generate_activation_token()
    send_email(current_user.email, '账户激活', 'mail/activation.html', user=current_user, token=token)
    flash('发送成功，您的邮箱 {email} 将会收到一封激活邮件，请在一小时内查收邮件进行账户激活'.format(email=current_user.email), 'success')
    return redirect(url_for('home.index'))


@account.route('/active/')
def active():
    token = request.args.get('token')
    data = User.load_activation_token(token)
    print data
    if not data:
        flash('激活连接不合法或已失效', 'danger')
        return redirect(url_for('home.index'))

    user_id = data.get('user_id')
    user = User.query.get(user_id)
    if not user:
        flash('该账户还未注册', 'danger')
        return redirect(url_for('account.register'))

    if user.status != USER_STATUS['new']:
        if user.status == USER_STATUS['active']:
            flash('账户已激活，请勿重复激活', 'info')
        elif user.status == USER_STATUS['frozen']:
            flash('账户已被冻结，无法激活', 'danger')
        return redirect(url_for('home.index'))

    user.status = USER_STATUS['active']
    db.session.add(user)
    db.session.commit()
    flash('账户激活成功', 'success')
    return redirect(url_for('account.login'))
