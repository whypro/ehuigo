# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.mail import Mail
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap


db = SQLAlchemy()

migrate = Migrate()

mail = Mail()

login_manager = LoginManager()
login_manager.login_view = 'account.login'
login_manager.login_message = '请先登录'
login_manager.login_message_category = "warning"

bootstrap = Bootstrap()
