# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from flask import Blueprint, render_template, request, redirect, url_for, abort, flash, g, current_app
from flask.ext.login import login_required, current_user

from ..extensions import db
from ..models import Manufacturer, Product, Question, Answer, Category, User
from ..helpers import create_uploader, send_email
from ..constants import QUESTION_CATEGORY, QUESTION_CATEGORY_REVERSED

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
        category_id = int(request.form.get('product-category'))
        product.category_id = category_id if category_id else None

        fs = request.files.get('product-photo')
        if fs:
            uploader = create_uploader()
            filename = uploader.save(fs)
            product.photo = filename

        db.session.add(product)
        db.session.commit()

        flash('保存成功', 'success')
        return redirect(url_for('admin.edit_product', product_id=product_id))

    categories = Category.query.all()
    return render_template('admin/product_detail.html', product=product, categories=categories)


@admin.route('/product/<int:product_id>/delete/')
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    manufacturer_id = product.manufacturer_id
    db.session.delete(product)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect(url_for('admin.show_products', manufacturer_id=manufacturer_id))


@admin.route('/questions/', defaults={'category': 'recycle'})
@admin.route('/questions/<category>/')
@login_required
def show_questions(category):
    if category not in QUESTION_CATEGORY.keys():
        abort(404)
    questions = Question.query.filter_by(category=QUESTION_CATEGORY[category]).all()
    return render_template('admin/questions.html', questions=questions, category=category)


@admin.route('/question/add/', methods=['POST'])
@login_required
def add_question():
    question_content = request.form.get('question-content')
    question_remark = request.form.get('question-remark')
    answer_contents = request.form.getlist('answer-content[]')
    answer_remarks = request.form.getlist('answer-remark[]')
    category = request.form.get('category')
    if not question_content or not answer_contents or category not in QUESTION_CATEGORY.keys():
        abort(400)

    question = Question(content=question_content, remark=question_remark, category=QUESTION_CATEGORY[category])
    db.session.add(question)
    for i, content in enumerate(answer_contents):
        answer = Answer(question=question, content=content, remark=answer_remarks[i])
        db.session.add(answer)
    db.session.commit()

    flash('添加成功', 'success')
    return redirect(url_for('admin.show_questions', category=category))


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
    return redirect(url_for('admin.show_questions', category=QUESTION_CATEGORY_REVERSED[question.category]))


@admin.route('/question/<question_id>/delete/')
@login_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect(url_for('admin.show_questions', category=QUESTION_CATEGORY_REVERSED[question.category]))


@admin.route('/product/<int:product_id>/recycle/edit/')
@login_required
def edit_recycle(product_id):
    product = Product.query.get_or_404(product_id)
    if not product.for_recycle:
        # 未设置 for_recycle
        flash('请先选中旧机回收选项', 'warning')
        return redirect(url_for('admin.show_products', manufacturer_id=product.manufacturer_id))

    questions = Question.query.filter_by(category=QUESTION_CATEGORY['recycle']).all()
    discounts = dict()
    for product_answer in product.product_recycle_answers:
        discounts[product_answer.answer_id] = product_answer.discount
    # print discounts
    # [{'choices': [], 'price': int}]

    return render_template('admin/recycle.html', product=product, questions=questions, discounts=discounts)


def test_answers(questions, discounts):
    pass


def __travel(questions):
    """深度优先遍历"""
    pass


@admin.route('/product/<int:product_id>/exchange/edit/')
@login_required
def edit_exchange(product_id):
    product = Product.query.get_or_404(product_id)
    if not product.for_exchange:
        # 未设置 for_exchange
        flash('请先选中以旧换新选项', 'warning')
        return redirect(url_for('admin.show_products', manufacturer_id=product.manufacturer_id))

    questions = Question.query.filter_by(category=QUESTION_CATEGORY['exchange']).all()
    discounts = dict()
    for product_answer in product.product_exchange_answers:
        discounts[product_answer.answer_id] = product_answer.discount

    return render_template('admin/exchange.html', product=product, questions=questions, discounts=discounts)


@admin.route('/send_test_mail/')
@login_required
def send_test_mail():
    if current_user.email:
        send_email(current_user.email, '测试邮件', 'mail/test.html', username=current_user.username)
        flash('测试邮件发送成功', 'success')
    return redirect(url_for('admin.index'))


# TODO: 加入角色系统之前的临时方法
@admin.before_request
@login_required
def before_request():
    if not current_user.status.is_admin:
        flash('权限不足', 'warning')
        return redirect(url_for('home.index'))


@admin.route('/categories/')
def show_categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)


@admin.route('/category/add/', methods=['POST'])
def add_category():
    name = request.form.get('category-name')
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return redirect(url_for('admin.show_categories'))


@admin.route('/category/<int:category_id>/delete/')
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('admin.show_categories'))


@admin.route('/users/')
def show_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)