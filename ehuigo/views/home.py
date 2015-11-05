# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort, current_app, send_from_directory, g
from flask.ext.login import login_user, logout_user, login_required

from ..extensions import db
from ..models import Manufacturer, Product, ProductAnswer
from ..models import User

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
        if price < 0: price = 0     # TODO: 变量加入数据库
        print price
        return jsonify(price=int(price))

    product = Product.query.get_or_404(product_id)
    return render_template('evaluate.html', product=product)


@home.route('/uploads/<filename>/')
@login_required
def send_upload_file(filename):
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename)


@home.route('/products/')
@home.route('/manufacturer/<int:manufacturer_id>/products/')
def show_products(manufacturer_id=None):
    if manufacturer_id:
        manufacturer = Manufacturer.query.get_or_404(manufacturer_id)
        products = Product.query.filter_by(manufacturer_id=manufacturer_id)
    else:
        manufacturer = None
        products = Product.query.all()
    return render_template('products.html', products=products, manufacturer=manufacturer)


@home.route('/manufacturers/')
def show_manufacturers():
    manufacturers = Manufacturer.query.all()
    return render_template('manufacturers.html', manufacturers=manufacturers)


@home.route('/login/', methods=['GET', 'POST'])
def login():
    # 已登录用户则返回首页
    if g.user.is_authenticated:
        return redirect(url_for('home.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(email=username, password=hashlib.sha1(password).hexdigest()).first()
        print user
        if user:
            login_user(user)
            return redirect(url_for('admin.index'))
    
    return render_template('account/login.html')


@home.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))
