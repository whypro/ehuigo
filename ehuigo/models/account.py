# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column('password', db.String(128), nullable=False)
    nickname = db.Column(db.String(20), unique=True)
    mobile = db.Column(db.String(20))
    reg_time = db.Column(db.DateTime, default=datetime.datetime.now)
    reg_ip = db.Column(db.String(20))
    status = db.Column(db.String(10), default='active')
    avatar = db.Column(db.String(255))

    # flask.ext.login
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
    # flask.ext.login end

    @property
    def password(self):
        raise AttributeError('raw_password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self._password, password)
