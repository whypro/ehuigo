# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort, current_app, send_from_directory

from ..extensions import db
from ..models import Manufacturer, Product, ProductAnswer

home = Blueprint('home', __name__)


@home.route('/')
def index():
    manufacturers = Manufacturer.query.limit(current_app.config['HOT_MANUFACTURER_NUM']).all()
    hot_products = Product.query.order_by(Product.price.desc()).limit(current_app.config['HOT_PRODUCT_NUM']).all()
    return render_template('index.html', manufacturers=manufacturers, hot_products=hot_products)


@home.route('/eval/<int:product_id>/', methods=['GET', 'POST'])
def evaluate(product_id):
    if request.method == 'POST':
        product = Product.query.get_or_404(product_id)
        price = product.price
        data = request.get_json()
        for answer_id in data['answers']:
            product_answer = ProductAnswer.query.filter_by(product_id=product_id, answer_id=answer_id).one()
            price += product_answer.discount    # 加负等于减正
        print price
        return jsonify(price=int(price))

    product = Product.query.get_or_404(product_id)
    return render_template('evaluate.html', product=product)


@home.route('/init/')
def init():
    db.create_all()
    return redirect(url_for('home.index'))


@home.route('/uploads/<filename>/')
def send_upload_file(filename):
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename)
