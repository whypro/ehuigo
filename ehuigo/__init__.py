# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from flask import Flask, flash, redirect, url_for, g
from flask.ext.login import LoginManager, current_user

from . import views
from .extensions import db, migrate
from .models import User


def create_app(config=None):
    app = Flask(__name__)

    # config
    app.config.from_object(config)

    # blueprint
    app.register_blueprint(views.home)
    # app.register_blueprint(views.post)
    # app.register_blueprint(views.member)
    app.register_blueprint(views.admin)

    # database & migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # logger
    init_app_logger(app)

    configure_flasklogin(app)
    config_before_request(app)


    return app


def init_app_logger(app):
    # logging

    file_handler = logging.FileHandler('flask.log')

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    )

    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.ERROR)
    app.logger.addHandler(file_handler)


def configure_flasklogin(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(uid):
        user = User.query.get(uid)
        return user

    @login_manager.unauthorized_handler
    def unauthorized():
        # flash('请先登录', 'warning')
        return redirect(url_for('home.login'))


def config_before_request(app):
    @app.before_request
    def before_request():
        g.user = current_user
