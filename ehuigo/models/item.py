# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy.ext.associationproxy import association_proxy
from flask import current_app

from ..extensions import db


class Manufacturer(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(20), nullable=False)    # 品牌名称
    alias = db.Column(db.Unicode(20))   # 品牌别名
    logo = db.Column(db.Unicode(200))   # 品牌 LOGO

    @property
    def logo_url(self):
        url = '/static/images/manufacturers/default.png'
        if self.logo:
            if self.logo.startswith('/') or self.logo.startswith('http'):
                url = self.logo
            else:
                url = '/' + current_app.config['UPLOAD_PREFIX'] + '/' + self.logo
        return url


class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id', ondelete='CASCADE'))  # 制造商 ID
    manufacturer = db.relationship('Manufacturer', backref=db.backref('products', passive_deletes=True))
    model = db.Column(db.Unicode(20))           # 型号
    version = db.Column(db.Unicode(20))         # 版本
    photo = db.Column(db.Unicode(200))          # 图片路径

    for_recycle = db.Column(db.Boolean, default=False)
    for_exchange = db.Column(db.Boolean, default=False)

    questions = association_proxy('product_questions', 'question')

    @property
    def photo_url(self):
        url = '/static/images/products/default.png'
        if self.photo:
            if self.photo.startswith('/') or self.photo.startswith('http'):
                url = self.photo
            else:
                url = '/' + current_app.config['UPLOAD_PREFIX'] + '/' + self.photo
        return url


class Price(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'))            # 物品 ID
    product = db.relationship('Product', backref=db.backref('price', uselist=False))
    recycle_max_price = db.Column(db.Numeric(10, 2), default=0)
    recycle_min_price = db.Column(db.Numeric(10, 2), default=0)
    exchange_price = db.Column(db.Numeric(10, 2), default=0)


class Album(object):

    id = ''
    product_id = ''
    photo = ''


class Question(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Unicode(60), nullable=False)            # 问题，如“成色”，“是否进水”


class Answer(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))        # 问题 ID
    question = db.relationship('Question', backref=db.backref('answers', passive_deletes=True))
    content = db.Column(db.Unicode(60), nullable=False)            # 回答内容
    description = db.Column(db.Unicode(100))        # 描述


class ProductQuestion(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'))            # 物品 ID
    product = db.relationship('Product', backref='product_questions')
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))        # 问题 ID
    question = db.relationship('Question')
    order = db.Column(db.Integer)              # 排序


class ProductAnswer(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'))     # 物品 ID
    product = db.relationship('Product', backref='product_answers')
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'))          # 回答 ID
    answer = db.relationship('Answer')
    discount = db.Column(db.Numeric(10, 2))           # 相应折扣
