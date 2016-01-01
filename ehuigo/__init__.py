# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from flask import Flask, render_template, request, jsonify
from flask.ext.sqlalchemy import get_debug_queries

from . import views
from .extensions import db, migrate, mail, login_manager, bootstrap
from .models import User

from config import config


def create_app(config_name):
    app = Flask(__name__)

    # config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # logger
    init_app_logger(app)

    # blueprint
    app.register_blueprint(views.home)
    app.register_blueprint(views.account)
    app.register_blueprint(views.admin)
    app.register_blueprint(views.api)
    app.register_blueprint(views.order)

    # database & migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # mail
    mail.init_app(app)

    login_manager.init_app(app)

    bootstrap.init_app(app)
    # print app.extensions['bootstrap']['cdns']

    config_request_handlers(app)
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
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)


def config_request_handlers(app):
    @app.before_request
    def before_request():
        pass
        # g.user = current_user

    @app.after_request
    def after_request(response):
        # 慢查询监视
        for query in get_debug_queries():
            if query.duration >= app.config['FLASK_SLOW_DB_QUERY_TIME']:
                app.logger.warning(
                    'Slow query: {0}\nParameters: {1}\nDuration: {2}\nContext: {3}\n'.format(
                        query.statement, query.parameters, query.duration, query.context
                    )
                )
        return response


def config_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            response = jsonify({'error': 'bad request'})
            response.status_code = 400
            return response
        return render_template('error/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            response = jsonify({'error': 'page not found'})
            response.status_code = 404
            return response
        return render_template('error/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            response = jsonify({'error': 'internal server error'})
            response.status_code = 500
            return response
        return render_template('error/500.html'), 500
