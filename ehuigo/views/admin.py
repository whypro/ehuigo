# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort, current_app
from werkzeug import secure_filename

from ..extensions import db
from ..models import Manufacturer, Product, Question, Answer

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
def index():
    return render_template('admin/index.html')


@admin.route('/manufacturers/')
def show_manufacturers():
    manufacturers = Manufacturer.query.all()
    return render_template('admin/manufacturers.html', manufacturers=manufacturers)

@admin.route('/manufacturer/add/', methods=['POST'])
def add_manufacturer():
    name = request.form.get('manufacturer-name')
    alias = request.form.get('manufacturer-alias')
    logo = request.form.get('manufacturer-logo')

    if not name:
        abort(400)

    if logo:
        f = request.files['manufacturer-logo']
        filename = secure_filename(f.filename)
        path = os.path.join(current_app.config['UPLOAD_PATH'], filename)
        print path
        f.save(path)
    else:
        filename = None

    manufacturer = Manufacturer(name=name, alias=alias, logo=filename)
    db.session.add(manufacturer)
    db.session.commit()

    return redirect(url_for('admin.show_manufacturers'))


@admin.route('/manufacturer/<int:manufacturer_id>/delete/')
def delete_manufacturer(manufacturer_id):
    manufacturer = Manufacturer.query.get_or_404(manufacturer_id)
    # remove manufacturer.logo
    path = os.path.join(current_app.config['UPLOAD_PATH'], manufacturer.logo)
    print path
    db.session.delete(manufacturer)
    db.session.commit()
    return redirect(url_for('admin.show_manufacturers'))


@admin.route('/manufacturer/<int:manufacturer_id>/products/')
def show_products(manufacturer_id):
    manufacturer = Manufacturer.query.get_or_404(manufacturer_id)
    products = Product.query.filter_by(manufacturer_id=manufacturer_id)
    return render_template('admin/products.html', products=products, manufacturer=manufacturer)


@admin.route('/product/add/', methods=['POST'])
def add_product():
    manufacturer_name = request.form.get('product-manufacturer')
    model = request.form.get('product-model')
    price = request.form.get('product-price')
    photo = request.form.get('product-photo')

    print manufacturer_name, model, price, photo

    return redirect(url_for('admin.show_products'))

@admin.route('/questions/')
def show_questions():
    questions = Question.query.all()
    return render_template('admin/questions.html', questions=questions)


@admin.route('/question/add/', methods=['POST'])
def add_question():
    question_content = request.form.get('question-content')
    answer_contents = request.form.getlist('answer-content[]')
    if not question_content or not answer_contents:
        abort(400)

    question = Question(content=question_content)
    db.session.add(question)
    for content in answer_contents:
        answer = Answer(question=question, content=content)
        db.session.add(answer)
    db.session.commit()

    return redirect(url_for('admin.show_questions'))


@admin.route('/question/<question_id>/delete/')
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('admin.show_questions'))


@admin.route('/product/<int:product_id>/evaluation/edit/')
def edit_evaluation(product_id):
    product = Product.query.get_or_404(product_id)
    questions = Question.query.all()
    return render_template('admin/evaluation.html', product=product, questions=questions)
