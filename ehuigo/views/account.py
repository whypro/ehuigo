# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Blueprint, redirect, request, url_for, render_template, g, flash
from flask.ext.login import login_user, logout_user, login_required

from ..models import User
from ..forms import RegisterForm


account = Blueprint('account', __name__, url_prefix='/account')


@account.route('/login/', methods=['GET', 'POST'])
def login():
    # 已登录用户则返回首页
    if g.user.is_authenticated():
        return redirect(url_for('home.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(email=username).first()
        # print user
        if user and user.verify_password(password):
            login_user(user)
            return redirect(request.args.get('next')) or redirect(url_for('admin.index'))
        else:
            flash('用户名或密码错误', 'danger')
            return redirect(url_for('account.login'))

    return render_template('account/login.html')


@account.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))


@account.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect('account.login')
    return render_template('account/register.html', form=form)
