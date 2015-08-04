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

    HOT_PRODUCT_NUM = 4
    HOT_MANUFACTURER_NUM = 6


class BAEConfig(Config):

    # 数据库配置
    DB_HOST = 'sqld.duapp.com'
    DB_DATABASE = 'kHeMtkVTtzsGvfbmEtLU'
    DB_USERNAME = 'AF28c466e7dd74686195abc876d4849b'
    DB_PASSWORD = '2b2f8ac70616dbea89fc2ac2312de1a9'
    DB_PORT = 4050

