# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os


class Config(object):
    SECRET_KEY = 'e-huigo'
    # JSON_SORT_KEY = False
    # JSONIFY_PRETTYPRINT_REGULAR = False

    # 数据库配置
    DB_HOST = 'localhost'
    DB_DATABASE = 'ehuigo'
    DB_USERNAME = 'root'
    DB_PASSWORD = 'whypro'
    DB_PORT = 3306

    # FLASK-SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = 'mysql://{username}:{password}@{host}:{port}/{database}?charset=utf8'.format(
        username=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_DATABASE
    )
    # Flask-SQLAlchemy Debugging Option
    # SQLALCHEMY_ECHO = True

    HOT_PRODUCT_NUM = 6
