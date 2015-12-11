# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort, current_app, flash
from werkzeug import secure_filename
from flask.ext.login import login_required

from ..extensions import db
from ..models import Manufacturer, Product, Question, Answer, ProductQuestion, ProductAnswer, Price
from ..helpers import create_uploader

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@login_required
def index():
    # return render_template('admin/index.html')
    return redirect(url_for('admin.show_manufacturers'))


@admin.route('/manufacturers/')
@login_required
def show_manufacturers():
    manufacturers = Manufacturer.query.all()
    return render_template('admin/manufacturers.html', manufacturers=manufacturers)

@admin.route('/manufacturer/add/', methods=['POST'])
@login_required
def add_manufacturer():
    name = request.form.get('manufacturer-name')
    alias = request.form.get('manufacturer-alias')

    if not name:
        abort(400)

    # print name, alias
    filename = None
    fs = request.files.get('manufacturer-logo')
    if fs:
        uploader = create_uploader()
        filename = uploader.save(fs)

    manufacturer = Manufacturer(name=name, alias=alias, logo=filename)
    db.session.add(manufacturer)
    db.session.commit()

    flash('添加成功', 'success')
    return redirect(url_for('admin.show_manufacturers'))


@admin.route('/manufacturer/<int:manufacturer_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_manufacturer(manufacturer_id):
    manufacturer = Manufacturer.query.get_or_404(manufacturer_id)
    if request.method == 'POST':
        name = request.form.get('manufacturer-name')
        alias = request.form.get('manufacturer-alias')

        if not name:
            abort(400)

        # print name, alias
        filename = None
        fs = request.files.get('manufacturer-logo')
        if fs:
            uploader = create_uploader()
            filename = uploader.save(fs)
            manufacturer.logo = filename

        manufacturer.name = name
        manufacturer.alias = alias

        db.session.add(manufacturer)
        db.session.commit()

        flash('保存成功', 'success')
        return redirect(url_for('admin.edit_manufacturer', manufacturer_id=manufacturer_id))

    return render_template('admin/manufacturer_detail.html', manufacturer=manufacturer)


@admin.route('/manufacturer/<int:manufacturer_id>/delete/')
@login_required
def delete_manufacturer(manufacturer_id):
    manufacturer = Manufacturer.query.get_or_404(manufacturer_id)
    # remove manufacturer.logo
    # path = os.path.join(current_app.config['UPLOAD_PATH'], manufacturer.logo)
    # print path
    db.session.delete(manufacturer)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect(url_for('admin.show_manufacturers'))


@admin.route('/manufacturer/<int:manufacturer_id>/products/')
@login_required
def show_products(manufacturer_id):
    manufacturer = Manufacturer.query.get_or_404(manufacturer_id)
    products = Product.query.filter_by(manufacturer_id=manufacturer_id)
    return render_template('admin/products.html', products=products, manufacturer=manufacturer)


@admin.route('/product/add/', methods=['POST'])
@login_required
def add_product():
    print request.form
    manufacturer_id = request.form.get('product-manufacturer')
    model = request.form.get('product-model')

    if not manufacturer_id or not model:
        abort(404)

    # print manufacturer_id, model
    filename = None
    fs = request.files.get('product-photo')
    if fs:
        uploader = create_uploader()
        filename = uploader.save(fs)

    manufacturer_id = int(manufacturer_id)
    manufacturer = Manufacturer.query.get_or_404(manufacturer_id)
    product = Product(manufacturer=manufacturer, model=model, version=None, photo=filename)
    db.session.add(product)
    db.session.commit()
    flash('添加成功', 'success')
    return redirect(url_for('admin.show_products', manufacturer_id=manufacturer_id))


@admin.route('/product/<int:product_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        model = request.form.get('product-model')
        product.model = model

        fs = request.files.get('product-photo')
        if fs:
            uploader = create_uploader()
            filename = uploader.save(fs)
            product.photo = filename

        db.session.add(product)
        db.session.commit()

        flash('保存成功', 'success')
        return redirect(url_for('admin.edit_product', product_id=product_id))

    return render_template('admin/product_detail.html', product=product)


@admin.route('/product/<int:product_id>/delete/')
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    manufacturer_id = product.manufacturer_id
    db.session.delete(product)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect(url_for('admin.show_products', manufacturer_id=manufacturer_id))


@admin.route('/questions/')
@login_required
def show_questions():
    questions = Question.query.all()
    return render_template('admin/questions.html', questions=questions)


@admin.route('/question/add/', methods=['POST'])
@login_required
def add_question():
    question_content = request.form.get('question-content')
    question_remark = request.form.get('question-remark')
    answer_contents = request.form.getlist('answer-content[]')
    answer_remarks = request.form.getlist('answer-remark[]')
    if not question_content or not answer_contents:
        abort(400)

    question = Question(content=question_content, remark=question_remark)
    db.session.add(question)
    for i, content in enumerate(answer_contents):
        answer = Answer(question=question, content=content, remark=answer_remarks[i])
        db.session.add(answer)
    db.session.commit()

    flash('添加成功', 'success')
    return redirect(url_for('admin.show_questions'))


@admin.route('/question/<int:question_id>/')
@login_required
def get_question(question_id):
    question = Question.query.get_or_404(question_id)
    question_dict = dict(id=question_id, content=question.content, remark=question.remark, answers=[])
    for answer in question.answers:
        question_dict['answers'].append(dict(id=answer.id, content=answer.content, remark=answer.remark))

    return jsonify(question_dict)


@admin.route('/question/<int:question_id>/edit/', methods=['POST'])
@login_required
def edit_question(question_id):
    question_content = request.form.get('question-content')
    question_remark = request.form.get('question-remark')
    answer_ids = request.form.getlist('answer-id[]')
    answer_contents = request.form.getlist('answer-content[]')
    answer_remarks = request.form.getlist('answer-remark[]')
    if not question_content or not answer_contents:
        abort(400)

    question = Question.query.get_or_404(question_id)
    question.content = question_content
    question.remark = question_remark
    db.session.add(question)
    for i, content in enumerate(answer_contents):
        answer = Answer.query.get(answer_ids[i])
        if not answer:
            answer = Answer(question=question, content=content, remark=answer_remarks[i])
        else:
            answer.content = content
            answer.remark = answer_remarks[i]
        db.session.add(answer)
        
    db.session.commit()

    flash('保存成功', 'success')
    return redirect(url_for('admin.show_questions'))


@admin.route('/question/<question_id>/delete/')
@login_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect(url_for('admin.show_questions'))


@admin.route('/product/<int:product_id>/recycle/edit/', methods=['GET', 'POST'])
@login_required
def edit_recycle(product_id):
    if request.method == 'POST':
        data = request.get_json()

        # 删除
        original_questions = ProductQuestion.query.filter_by(product_id=product_id).all()
        for question in original_questions:
            if question.id not in data['questions']:
                db.session.delete(question)

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

        price.recycle_max_price = data['recycle_max_price']
        price.recycle_min_price = data['recycle_min_price']
        db.session.add(price)

        db.session.commit()
        flash('保存成功', 'success')
        return jsonify(status=200)
        #product_question = ProductQuestion(product=product, question=question, order=order)

    product = Product.query.get_or_404(product_id)
    if not product.for_recycle:
        # 未设置 for_recycle
        flash('请先选中旧机回收选项', 'warning')
        return redirect(url_for('admin.show_products', manufacturer_id=product.manufacturer_id))

    questions = Question.query.all()
    discounts = dict()
    for product_answer in ProductAnswer.query.filter_by(product_id=product_id).all():
        discounts[product_answer.answer_id] = product_answer.discount
    # print discounts
    # [{'choices': [], 'price': int}]

    return render_template('admin/recycle.html', product=product, questions=questions, discounts=discounts)


def test_answers(questions, discounts):
    pass

def __travel(questions):
    """深度优先遍历"""
    pass


@admin.route('/product/<int:product_id>/exchange/edit/', methods=['GET', 'POST'])
@login_required
def edit_exchange(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        exchange_price = request.form.get('exchange-price', '0')
        exchange_price = float(exchange_price)
        product.price.exchange_price = exchange_price
        db.session.add(product)
        db.session.commit()
        flash('保存成功', 'success')
        return redirect(url_for('admin.edit_exchange', product_id=product_id))

    if not product.for_exchange:
        # 未设置 for_exchange
        flash('请先选中以旧换新选项', 'warning')
        return redirect(url_for('admin.show_products', manufacturer_id=product.manufacturer_id))

    return render_template('admin/exchange.html', product=product)


@admin.route('/product/<int:product_id>/recycle/<action>/')
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

    return jsonify(status=200)


@admin.route('/product/<int:product_id>/exchange/<action>/')
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

    return jsonify(status=200)
