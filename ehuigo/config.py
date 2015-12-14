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

    UPLOAD_PATH = os.path.join(os.path.realpath('.'), 'uploads')
    UPLOAD_PREFIX = 'uploads'
    UPLOAD_ALLOWED_EXT = ['jpg', 'png', 'bmp', 'gif']
    UPLOAD_MAX_SIZE = 4 * 1024 * 1024    # 4M

    MAIL_SERVER = 'smtp.126.com'
    MAIL_PORT = 994
    MAIL_USE_SSL = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''


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

    DEBUG = True


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

    OSS_ENDPOINT = 'static.ehuigo.cn'
    KEY_ID = 'xi0qjghwneAdNtkQ'
    KEY_SECRET = '8z1MUO3NQt6oJVdQD0qAxNaXBnWH9D'
    OSS_BUCKET_NAME = 'ehuigo'

