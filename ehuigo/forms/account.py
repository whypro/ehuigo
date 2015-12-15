# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from wtforms import ValidationError

from ..models import User
from ..constants import MAX_LENGTH


class RegisterForm(Form):
    email = StringField('Email', validators=[InputRequired(), Length(1, MAX_LENGTH['email']), Email()])
    username = StringField('用户名', validators=[InputRequired(), Length(1, MAX_LENGTH['username'])])
    password = PasswordField('密码', validators=[InputRequired(), Length(1, MAX_LENGTH['password']), EqualTo('password_confirm', message='密码不一致')])
    password_confirm = PasswordField('密码确认', validators=[InputRequired()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被注册')
