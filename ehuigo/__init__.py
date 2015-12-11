# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from flask import Flask, flash, redirect, url_for, g, render_template
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

    config_flask_login(app)
    config_before_request(app)
    config_error_handlers(app)


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


def config_flask_login(app):
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


def config_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('error/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error/500.html'), 500
