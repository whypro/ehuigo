# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Blueprint, redirect, request, url_for, render_template, session, flash, abort
from flask.ext.login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_

from ..models import User, UserStatus
from ..forms import RegisterForm, RegisterByEmailForm, UserProfileForm, UserSecurityForm
from ..extensions import db
from ..helpers import send_email, get_client_ip, create_uploader


account = Blueprint('account', __name__, url_prefix='/account')


@account.route('/login/', methods=['GET', 'POST'])
def login():
    # 已登录用户则返回首页
    if current_user.is_authenticated():
        return redirect(request.args.get('next') or url_for('admin.index'))

    if request.method == 'POST':
        login_name = request.form.get('login-name')
        password = request.form.get('password')
        user = User.query.filter(or_(User.email==login_name, User.cellphone==login_name, User.username==login_name)).first()
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
    """通过手机号注册"""
    # 已登录用户则返回首页
    if current_user.is_authenticated():
        return redirect(url_for('admin.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            # email=form.email.data,
            # username=form.username.data,
            password=form.password.data,
            cellphone=form.cellphone.data,
            reg_ip=get_client_ip(),
            status=UserStatus(cellphone_confirmed=True)
        )
        db.session.add(user)
        db.session.commit()
        # token = user.generate_activation_token()
        # send_email(user.email, '账户激活', 'mail/activation.html', user=user, token=token)
        # flash('注册成功，您的邮箱 {email} 将会收到一封激活邮件，请在一小时内查收邮件进行账户激活'.format(email=user.email), 'success')
        flash('注册成功', 'success')
        return redirect(url_for('account.login'))
    return render_template('account/register.html', form=form)


@account.route('/register/by_email/', methods=['GET', 'POST'])
def register_by_email():
    """通过邮箱注册"""
    # 已登录用户则返回首页
    if current_user.is_authenticated():
        return redirect(url_for('admin.index'))

    form = RegisterByEmailForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            # username=form.username.data,
            password=form.password.data,
            # cellphone=form.cellphone.data,
            reg_ip=get_client_ip(),
            status=UserStatus()
        )
        db.session.add(user)
        db.session.commit()
        token = user.generate_activation_token()
        send_email(user.email, '账户激活', 'mail/activation.html', user=user, token=token)
        flash('注册成功，您的邮箱 {email} 将会收到一封激活邮件，请在一小时内查收邮件进行账户激活'.format(email=user.email), 'success')
        return redirect(url_for('account.login'))
    return render_template('account/register_by_email.html', form=form)


@account.route('/activate/')
def activate():
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

    if user.status.email_confirmed:
        flash('账户已激活，请勿重复激活', 'info')
        return redirect(url_for('home.index'))
    # elif user.status == USER_STATUS['frozen']:
    #     flash('账户已被冻结，无法激活', 'danger')

    user.status.email_confirmed = True
    # user_status = UserStatus.query.filter(user_id=user.id)
    db.session.add(user)
    db.session.commit()
    flash('账户激活成功', 'success')
    return redirect(url_for('account.login'))


@account.route('/activation/resend/')
@login_required
def resend_activation():
    token = current_user.generate_activation_token()
    send_email(current_user.email, '账户激活', 'mail/activation.html', user=current_user, token=token)
    flash('发送成功，您的邮箱 {email} 将会收到一封激活邮件，请在一小时内查收邮件进行账户激活'.format(email=current_user.email), 'success')
    return redirect(url_for('home.index'))


def show_profile():
    pass


@account.route('/<int:user_id>/profile/edit/', methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    if user_id != current_user.id:
        abort(403)

    user = User.query.get_or_404(user_id)
    form = UserProfileForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        fs = form.avatar.data
        if fs:
            uploader = create_uploader()
            filename = uploader.save(fs)
            user.avatar = filename
        db.session.add(user)
        db.session.commit()

        flash('保存成功', 'success')
        return redirect(url_for('account.edit_profile', user_id=user_id))

    return render_template('account/profile_edit.html', form=form, user=user)


@account.route('/<int:user_id>/security/edit/', methods=['GET', 'POST'])
@login_required
def edit_security(user_id):
    if user_id != current_user.id:
        abort(403)

    user = User.query.get_or_404(user_id)
    form = UserSecurityForm(obj=user)
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()

        flash('修改成功', 'success')
        return redirect(url_for('account.edit_security', user_id=user_id))

    return render_template('account/security_edit.html', form=form)
