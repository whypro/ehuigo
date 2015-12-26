# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy import and_
from sqlalchemy.ext.associationproxy import association_proxy
from flask import current_app

from ..extensions import db
from ..constants import MAX_LENGTH, QUESTION_CATEGORY


class Manufacturer(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(MAX_LENGTH['manufacturer_name']), nullable=False)    # 品牌名称
    alias = db.Column(db.Unicode(MAX_LENGTH['manufacturer_name']))   # 品牌别名
    logo = db.Column(db.Unicode(MAX_LENGTH['path']))   # 品牌 LOGO

    @property
    def logo_url(self):
        url = '/static/images/manufacturers/default.png'
        if self.logo:
            if self.logo.startswith('/') or self.logo.startswith('http'):
                url = self.logo
            else:
                url = '/' + current_app.config['UPLOAD_PREFIX'] + '/' + self.logo
        return url

    products = db.relationship('Product', backref='manufacturer', passive_deletes=True)


class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id', ondelete='CASCADE'))  # 制造商 ID
    model = db.Column(db.Unicode(MAX_LENGTH['product_model']))           # 型号
    version = db.Column(db.Unicode(MAX_LENGTH['product_version']))         # 版本
    photo = db.Column(db.Unicode(MAX_LENGTH['path']))          # 图片路径

    for_recycle = db.Column(db.Boolean, default=False)
    for_exchange = db.Column(db.Boolean, default=False)

    @property
    def photo_url(self):
        url = '/static/images/products/default.png'
        if self.photo:
            if self.photo.startswith('/') or self.photo.startswith('http'):
                url = self.photo
            else:
                url = '/' + current_app.config['UPLOAD_PREFIX'] + '/' + self.photo
        return url

    price = db.relationship('Price', backref='product', uselist=False, passive_deletes=True)

    product_recycle_questions = db.relationship(
        'ProductQuestion',
        primaryjoin='and_(Question.category=={0}, ProductQuestion.question_id==Question.id, ProductQuestion.product_id==Product.id)'.format(QUESTION_CATEGORY['recycle']),
        passive_deletes=True
    )
    product_exchange_questions = db.relationship(
        'ProductQuestion',
        primaryjoin='and_(Question.category=={0}, ProductQuestion.question_id==Question.id, ProductQuestion.product_id==Product.id)'.format(QUESTION_CATEGORY['exchange']),
        passive_deletes=True
    )
    recycle_questions = association_proxy('product_recycle_questions', 'question')
    exchange_questions = association_proxy('product_exchange_questions', 'question')

    product_recycle_answers = db.relationship(
        'ProductAnswer',
        primaryjoin='and_(Question.category=={0}, Answer.question_id==Question.id, ProductAnswer.answer_id==Answer.id, ProductAnswer.product_id==Product.id)'.format(QUESTION_CATEGORY['recycle']),
        passive_deletes=True
    )
    product_exchange_answers = db.relationship(
        'ProductAnswer',
        primaryjoin='and_(Question.category=={0}, Answer.question_id==Question.id, ProductAnswer.answer_id==Answer.id, ProductAnswer.product_id==Product.id)'.format(QUESTION_CATEGORY['exchange']),
        passive_deletes=True
    )

    # product_answers = db.relationship('ProductAnswer', backref='product', passive_deletes=True)


class Price(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'))            # 物品 ID
    recycle_max_price = db.Column(db.Numeric(10, 2), default=0)
    recycle_min_price = db.Column(db.Numeric(10, 2), default=0)
    exchange_price = db.Column(db.Numeric(10, 2), default=0)
    jd_price = db.Column(db.Numeric(10, 2))
    official_price = db.Column(db.Numeric(10, 2))


class Album(object):

    id = ''
    product_id = ''
    photo = ''


class Question(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Unicode(MAX_LENGTH['question_content']), nullable=False)     # 问题，如“成色”，“是否进水”
    remark = db.Column(db.Unicode(MAX_LENGTH['question_remark']))     # 备注
    category = db.Column(db.Integer, default=QUESTION_CATEGORY['recycle'])

    answers = db.relationship('Answer', backref='question', passive_deletes=True, lazy='joined')


class Answer(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))        # 问题 ID
    content = db.Column(db.Unicode(MAX_LENGTH['answer_content']), nullable=False)            # 回答内容
    remark = db.Column(db.Unicode(MAX_LENGTH['answer_remark']))        # 备注


class ProductQuestion(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'))            # 物品 ID
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))        # 问题 ID
    question = db.relationship('Question')
    order = db.Column(db.Integer)              # 排序


class ProductAnswer(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'))     # 物品 ID
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'))          # 回答 ID
    answer = db.relationship('Answer')
    discount = db.Column(db.Numeric(10, 2))           # 相应折扣
