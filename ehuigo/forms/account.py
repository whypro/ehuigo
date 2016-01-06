# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import session
from flask.ext.login import current_user
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Optional, Regexp, DataRequired
from wtforms import ValidationError

from ..models import User
from ..constants import MAX_LENGTH, REG_EXP_PHONE


class RegisterForm(Form):
    cellphone = StringField('手机号', validators=[
        InputRequired(),
        Length(1, MAX_LENGTH['cellphone'], '长度不合法'),
        Regexp(REG_EXP_PHONE, message='无效的手机号码')
    ])
    password = PasswordField('密码', validators=[
        InputRequired(),
        Length(1, MAX_LENGTH['password'], '长度不合法'),
        EqualTo('password_confirm', message='两次输入的密码不一致')
    ])
    password_confirm = PasswordField('密码确认', validators=[InputRequired()])
    sms_captcha = StringField(
        u'验证码',
        validators=[InputRequired(message=u'请输入短信验证码')]
    )
    # image_captcha = StringField(
    #     u'验证码',
    #     validators=[InputRequired(message=u'请输入验证码')]
    # )
    submit = SubmitField('注册')

    def validate_cellphone(self, field):
        if User.query.filter_by(cellphone=field.data).first():
            raise ValidationError('该手机号已注册')

    # def validate_image_captcha(self, field):
    #     if field.data != session.pop('image_captcha'):
    #         raise ValidationError('验证码不正确')

    def validate_sms_captcha(self, field):
        if self.cellphone != session['sms_captcha']['cellphone'] or field.data.upper() != session['sms_captcha']['captcha']:
            raise ValidationError('短信验证码不正确')


class RegisterByEmailForm(Form):
    # username = StringField('用户名', validators=[
    #     InputRequired(),
    #     Length(1, MAX_LENGTH['username'], '长度不合法'),
    #     Regexp('[\u4e00-\u9fa5A-Za-z0-9_]+$', message='用户名不能包含除简体汉字、字母、数字和下划线之外的字符')
    # ])
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
    # cellphone = StringField('手机号', validators=[
    #     Optional(),
    #     Length(1, MAX_LENGTH['cellphone'], '长度不合法'),
    #     Regexp(REG_EXP_PHONE, message='无效的手机号码')
    # ])
    image_captcha = StringField(
        u'验证码',
        validators=[InputRequired(message=u'请输入图片验证码')]
    )
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')

    # def validate_username(self, field):
    #     if User.query.filter_by(username=field.data).first():
    #         raise ValidationError('该用户名已被注册')

    def validate_image_captcha(self, field):
        # print field.data.upper(), session['image_captcha']
        if field.data.upper() != session['image_captcha']:
            raise ValidationError('验证码不正确')


class UserProfileForm(Form):
    username = StringField('用户名', validators=[
        InputRequired(),
        Length(1, MAX_LENGTH['username'], '长度不合法'),
        Regexp('[\u4e00-\u9fa5A-Za-z0-9_]+$', message='用户名不能包含除简体汉字、字母、数字和下划线之外的字符')
    ])
    # cellphone = StringField('手机号', validators=[
    #     InputRequired(),
    #     Length(1, MAX_LENGTH['cellphone'], '长度不合法'),
    #     Regexp(REG_EXP_PHONE, message='无效的手机号码')
    # ])
    # email = StringField('电子邮箱', validators=[
    #     InputRequired(),
    #     Length(1, MAX_LENGTH['email'], '长度不合法'),
    #     Email('无效的邮箱格式')
    # ])
    avatar = FileField('头像')
    submit = SubmitField('保存')

    def validate_username(self, field):
        if field.data != current_user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被注册')


class UserProfileCellphoneForm(Form):
    cellphone = StringField('手机号', validators=[
        InputRequired(),
        Length(1, MAX_LENGTH['cellphone'], '长度不合法'),
        Regexp(REG_EXP_PHONE, message='无效的手机号码')
    ])
    sms_captcha = StringField(
        u'短信验证码',
        validators=[InputRequired(message=u'请输入短信验证码')]
    )
    submit = SubmitField('保存')

    def validate_cellphone(self, field):
        if field.data == current_user.cellphone and current_user.status.cellphone_confirmed:
            raise ValidationError('该手机号已绑定现有账户')
        elif User.query.filter_by(cellphone=field.data).first():
            raise ValidationError('该手机号已绑定其他账户')

    def validate_sms_captcha(self, field):
        print self.cellphone.data
        print session['sms_captcha']['cellphone']
        print field.data.upper()
        print session['sms_captcha']['captcha']
        if self.cellphone.data != session['sms_captcha']['cellphone'] or field.data.upper() != session['sms_captcha']['captcha']:
            raise ValidationError('短信验证码不正确')


class UserSecurityForm(Form):
    password_old = PasswordField('原密码', validators=[InputRequired()])
    password = PasswordField('新密码', validators=[
        InputRequired(),
        Length(1, MAX_LENGTH['password'], '长度不合法'),
        EqualTo('password_confirm', message='两次输入的密码不一致')
    ])
    password_confirm = PasswordField('密码确认', validators=[InputRequired()])
    submit = SubmitField('修改')

    def validate_password_old(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('原密码不正确')
