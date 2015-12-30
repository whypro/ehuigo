# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'ehuigo'
    # JSON_SORT_KEY = False
    # JSONIFY_PRETTYPRINT_REGULAR = False

    HOT_PRODUCT_NUM = 4
    HOT_MANUFACTURER_NUM = 6

    UPLOAD_PATH = os.path.join(basedir, 'uploads')
    UPLOAD_PREFIX = 'uploads'
    UPLOAD_ALLOWED_EXT = ['jpg', 'png', 'bmp', 'gif']
    UPLOAD_MAX_SIZE = 4 * 1024 * 1024    # 4M

    # SQLAlchemy 慢查询日志
    SQLALCHEMY_RECORD_QUERIES = True
    FLASK_SLOW_DB_QUERY_TIME = 0.5

    MAIL_SERVER = 'smtp.mxhichina.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'noreply@ehuigo.cn'
    MAIL_PASSWORD = ''

    EHUIGO_MAIL_SENDER = '易回购 <noreply@ehuigo.cn>'
    EHUIGO_ADMINS = ['whypro@live.cn']

    # 云通讯配置
    YUNTONGXUN_BASE_URL = 'https://sandboxapp.cloopen.com:8883'
    YUNTONGXUN_ACCOUNT_SID = ''
    YUNTONGXUN_AUTH_TOKEN = ''
    YUNTONGXUN_APP_ID = ''

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
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

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # Flask-SQLAlchemy Debugging Option
    SQLALCHEMY_ECHO = True

    BOOTSTRAP_USE_MINIFIED = False
    BOOTSTRAP_SERVE_LOCAL = True


class BAEConfig(Config):

    # 数据库配置
    DB_HOST = 'sqld.duapp.com'
    DB_DATABASE = 'kHeMtkVTtzsGvfbmEtLU'
    DB_USERNAME = 'AF28c466e7dd74686195abc876d4849b'
    DB_PASSWORD = '2b2f8ac70616dbea89fc2ac2312de1a9'
    DB_PORT = 4050

    # FLASK-SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = 'mysql://{username}:{password}@{host}:{port}/{database}?charset=utf8'.format(
        username=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_DATABASE
    )

    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ACEConfig(Config):

    # 数据库配置
    DB_HOST = 'rds7z20k1nqpnmd558xy.mysql.rds.aliyuncs.com'
    DB_DATABASE = ''
    DB_USERNAME = ''
    DB_PASSWORD = ''
    DB_PORT = 3306

    # FLASK-SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = 'mysql://{username}:{password}@{host}:{port}/{database}?charset=utf8'.format(
        username=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_DATABASE
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    OSS_ENDPOINT = 'static.ehuigo.cn'
    KEY_ID = ''
    KEY_SECRET = ''
    OSS_BUCKET_NAME = 'ehuigo'


class TestConfig(Config):
    # 数据库配置
    # FLASK-SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'ehuigo.sqlite')

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    TESTING = True


config = {
    'development': DevelopmentConfig,
    'bae': BAEConfig,
    'ace': ACEConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig,
}
