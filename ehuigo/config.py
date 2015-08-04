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

    # Flask-SQLAlchemy Debugging Option
    # SQLALCHEMY_ECHO = True

    HOT_PRODUCT_NUM = 4
    HOT_MANUFACTURER_NUM = 6

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # FLASK-SQLALCHEMY
        uri = 'mysql://{username}:{password}@{host}:{port}/{database}?charset=utf8'.format(
            username=self.DB_USERNAME,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_DATABASE
        )
        return uri


class BAEConfig(Config):

    # 数据库配置
    DB_HOST = 'sqld.duapp.com'
    DB_DATABASE = 'kHeMtkVTtzsGvfbmEtLU'
    DB_USERNAME = 'AF28c466e7dd74686195abc876d4849b'
    DB_PASSWORD = '2b2f8ac70616dbea89fc2ac2312de1a9'
    DB_PORT = 4050

    DEBUG = True
