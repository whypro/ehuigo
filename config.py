# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'ehuigo'
    # JSON_SORT_KEY = False
    # JSONIFY_PRETTYPRINT_REGULAR = False

    # Flask-SQLAlchemy Debugging Option
    # SQLALCHEMY_ECHO = True

    HOT_PRODUCT_NUM = 4
    HOT_MANUFACTURER_NUM = 6

    UPLOAD_PATH = os.path.join(basedir, 'uploads')
    UPLOAD_PREFIX = 'uploads'
    UPLOAD_ALLOWED_EXT = ['jpg', 'png', 'bmp', 'gif']
    UPLOAD_MAX_SIZE = 4 * 1024 * 1024    # 4M

    MAIL_SERVER = 'smtp.126.com'
    MAIL_PORT = 994
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'whypro'
    MAIL_PASSWORD = ''

    EHUIGO_MAIL_SENDER = '易回购 <whypro@126.com>'

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
    DB_DATABASE = 'rjpa045c4i94u4nz'
    DB_USERNAME = 'rjpa045c4i94u4nz'
    DB_PASSWORD = '20151105'
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
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    OSS_ENDPOINT = 'static.ehuigo.cn'
    KEY_ID = 'xi0qjghwneAdNtkQ'
    KEY_SECRET = '8z1MUO3NQt6oJVdQD0qAxNaXBnWH9D'
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
