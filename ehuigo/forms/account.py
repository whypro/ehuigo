# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Optional, Regexp, DataRequired
from wtforms import ValidationError

from ..models import User
from ..constants import MAX_LENGTH


class RegisterForm(Form):
    username = StringField('用户名', validators=[
        InputRequired(),
        Length(1, MAX_LENGTH['username'], '长度不合法'),
        Regexp('[\u4e00-\u9fa5A-Za-z0-9_]+$', message='用户名不能包含除简体汉字、字母、数字和下划线之外的字符')
    ])
    email = StringField('电子邮箱', validators=[
        InputRequired(),
        Length(1, MAX_LENGTH['email'], '长度不合法'),
        Email('无效的邮箱格式')
    ])
    password = PasswordField('密码', validators=[
        InputRequired(),
        Length(1, MAX_LENGTH['password'], '长度不合法'),
        EqualTo('password_confirm', message='两次输入的密码不一致')
    ])
    password_confirm = PasswordField('密码确认', validators=[InputRequired()])
    mobile = StringField('手机', validators=[
        Optional(),
        Length(1, MAX_LENGTH['mobile'], '长度不合法'),
        Regexp('^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$', message='无效的手机号码')
    ])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被注册')
