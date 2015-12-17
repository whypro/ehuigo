# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from flask import Flask, redirect, url_for, g, render_template
from flask.ext.login import LoginManager, current_user
from flask.ext.bootstrap import Bootstrap

from . import views
from .extensions import db, migrate, mail, login_manager
from .models import User

from config import config


def create_app(config_name):
    app = Flask(__name__)

    # config
    app.config.from_object(config[config_name])

    # blueprint
    app.register_blueprint(views.home)
    app.register_blueprint(views.account)
    app.register_blueprint(views.admin)
    app.register_blueprint(views.api)

    # database & migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # mail
    mail.init_app(app)

    login_manager.init_app(app)

    Bootstrap(app)
    # print app.extensions['bootstrap']['cdns']

    # logger
    init_app_logger(app)

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
