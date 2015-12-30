# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask.ext.login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer
from itsdangerous import BadSignature, SignatureExpired

from ..extensions import db, login_manager
from ..constants import MAX_LENGTH


class UserStatus(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    cellphone_confirmed = db.Column(db.Boolean, default=False)
    email_confirmed = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    banned = db.Column(db.Boolean, default=False)


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(MAX_LENGTH['email']), unique=True, nullable=False)
    _password = db.Column('password', db.String(MAX_LENGTH['password']), nullable=False)
    username = db.Column(db.String(MAX_LENGTH['username']), unique=True)
    cellphone = db.Column(db.String(MAX_LENGTH['cellphone']), unique=True)
    reg_time = db.Column(db.DateTime, default=datetime.datetime.now)
    reg_ip = db.Column(db.String(MAX_LENGTH['ip']))
    status = db.relationship('UserStatus', passive_deletes=True, uselist=False)
    avatar = db.Column(db.String(MAX_LENGTH['path']))

    @property
    def password(self):
        raise AttributeError('raw_password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self._password, password)

    def generate_activation_token(self, expiration=3600):
        # 生成账户激活 token
        s = TJWSSerializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'user_id': self.id})

    @staticmethod
    def load_activation_token(token):
        # 根据 token 激活用户
        s = TJWSSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired) as e:
            print e
            return None

        return data


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



