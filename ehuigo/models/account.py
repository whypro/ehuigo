# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from ..extensions import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
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
