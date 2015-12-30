# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from flask import Blueprint, jsonify, abort, flash, request, session
from flask.ext.login import login_required

from ..models import Question, Product, Price, ProductQuestion, ProductAnswer
from ..extensions import db
from ..constants import QUESTION_CATEGORY, REG_EXP_PHONE
from ..helpers import gen_captcha_str, send_sms

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/question/<int:question_id>/')
@login_required
def get_question(question_id):
    question = Question.query.get_or_404(question_id)
    question_dict = dict(id=question_id, content=question.content, remark=question.remark, answers=[])
    for answer in question.answers:
        question_dict['answers'].append(dict(id=answer.id, content=answer.content, remark=answer.remark))

    return jsonify(question_dict)


@api.route('/product/<int:product_id>/recycle/<action>/')
@login_required
def set_recycle_product(product_id, action):
    if action not in ('set', 'unset'):
        abort(400)

    p = Product.query.get_or_404(product_id)
    p.for_recycle = True if action == 'set' else False
    db.session.add(p)
    price = Price.query.filter_by(product_id=product_id).first()
    if action == 'set' and not price:
        price = Price(product_id=product_id)
        db.session.add(price)
    db.session.commit()

    return jsonify()


@api.route('/product/<int:product_id>/exchange/<action>/')
@login_required
def set_exchange_product(product_id, action):
    if action not in ('set', 'unset'):
        abort(400)

    p = Product.query.get_or_404(product_id)
    p.for_exchange = True if action == 'set' else False
    db.session.add(p)
    price = Price.query.filter_by(product_id=product_id).first()
    if action == 'set' and not price:
        price = Price(product_id=product_id)
        db.session.add(price)
    db.session.commit()

    return jsonify()


@api.route('/product/<int:product_id>/<category>/edit/', methods=['POST'])
@login_required
def edit_product_qa(product_id, category):
    if category not in QUESTION_CATEGORY.keys():
        abort(404)

    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    # 删除
    if category == 'recycle':
        for product_question in product.product_recycle_questions:
            if product_question.id not in data['questions']:
                db.session.delete(product_question)
    elif category == 'exchange':
        for product_question in product.product_exchange_questions:
            if product_question.id not in data['questions']:
                db.session.delete(product_question)

    for order, question_id in enumerate(data['questions'], start=1):
        question_id = int(question_id)
        product_question = ProductQuestion.query.filter_by(product_id=product_id, question_id=question_id).first()
        if not product_question:
            product_question = ProductQuestion(product_id=product_id, question_id=question_id)
        product_question.order = order
        db.session.add(product_question)

    db.session.commit()

    for answer in data['answers']:
        answer_id = int(answer[0])
        discount = int(answer[1])
        product_answer = ProductAnswer.query.filter_by(product_id=product_id, answer_id=answer_id).first()
        if not product_answer:
            product_answer = ProductAnswer(product_id=product_id, answer_id=answer_id)
        product_answer.discount = discount
        db.session.add(product_answer)

    price = Price.query.filter_by(product_id=product_id).first()
    if not price:
        price = Price(product_id=product_id)

    if category == 'recycle':
        price.recycle_max_price = data['recycle_max_price']
        price.recycle_min_price = data['recycle_min_price']
    elif category == 'exchange':
        price.exchange_price = data['exchange_price']
        price.member_price = data['member_price']
        price.jd_price = data['jd_price']
        price.official_price = data['official_price']
        price.brief_intro = data['brief_intro']

    db.session.add(price)
    db.session.commit()
    flash('保存成功', 'success')
    return jsonify()


@api.route('/product/<int:product_id>/evaluate/', methods=['POST'])
def evaluate(product_id):
    product = Product.query.get_or_404(product_id)
    price = product.price.recycle_max_price
    min_price = product.price.recycle_min_price
    data = request.get_json()
    for answer_id in data['answers']:
        product_answer = ProductAnswer.query.filter_by(product_id=product_id, answer_id=answer_id).one()
        price += product_answer.discount    # 加负等于减正
    if price < min_price: price = min_price
    print price
    return jsonify(price=int(price))


@api.route('/product/<int:product_id>/quote/', methods=['POST'])
def quote(product_id):
    product = Product.query.get_or_404(product_id)
    price = product.price.exchange_price
    data = request.get_json()
    for answer_id in data['answers']:
        product_answer = ProductAnswer.query.filter_by(product_id=product_id, answer_id=answer_id).one()
        price += product_answer.discount    # 加负等于减正
    print price
    return jsonify(price=int(price))


@api.route('/captcha/sms/send/', methods=['POST'])
def send_sms_captcha():
    # return jsonify()
    SMS_CAPTCHA_TEMPLATE_ID = 1
    SMS_CAPTCHA_EXPIRE = 5
    data = request.get_json()
    phone = data['phone']
    image_captcha = data['image_captcha'].upper()
    # check phone
    if not re.match(REG_EXP_PHONE, phone):
        abort(400)

    # print image_captcha, session['image_captcha']
    if image_captcha != session.pop('image_captcha', None):
        abort(401)

    captcha_str = gen_captcha_str(6, digits_only=True)
    session['sms_captcha'] = captcha_str.upper()
    resp_json = send_sms(
        [phone],
        template_id=SMS_CAPTCHA_TEMPLATE_ID,
        template_data=[captcha_str, SMS_CAPTCHA_EXPIRE]
    )
    return jsonify(resp_json)
