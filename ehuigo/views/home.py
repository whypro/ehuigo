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
    hot_products = Product.query.filter_by(for_recycle=True).limit(current_app.config['HOT_PRODUCT_NUM']).all()
    return render_template('index.html', manufacturers=manufacturers, hot_products=hot_products)


@home.route('/recycle/product/<int:product_id>/evaluate/', methods=['GET', 'POST'])
def evaluate(product_id):
    if request.method == 'POST':
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

    product = Product.query.get_or_404(product_id)
    return render_template('home/recycle/product_detail.html', product=product)


@home.route('/uploads/<filename>/')
def send_upload_file(filename):
    if 'OSS_ENDPOINT' in current_app.config:
        url = 'http://' + current_app.config['OSS_ENDPOINT'] + '/' + filename
        return redirect(url)
    else:
        return send_from_directory(current_app.config['UPLOAD_PATH'], filename)


@home.route('/recycle/')
@home.route('/recycle/manufacturer/<int:manufacturer_id>/')
def show_recycle_products(manufacturer_id=None):
    if manufacturer_id:
        manufacturer = Manufacturer.query.get_or_404(manufacturer_id)
        products = Product.query.filter_by(manufacturer_id=manufacturer_id, for_recycle=True).all()
    else:
        manufacturer = None
        products = Product.query.filter_by(for_recycle=True).all()
    return render_template('home/recycle/products.html', products=products, manufacturer=manufacturer)


@home.route('/exchange/')
@home.route('/exchange/manufacturer/<int:manufacturer_id>/')
def show_exchange_products(manufacturer_id=None):
    if manufacturer_id:
        manufacturer = Manufacturer.query.get_or_404(manufacturer_id)
        products = Product.query.filter_by(manufacturer_id=manufacturer_id, for_exchange=True).all()
    else:
        manufacturer = None
        products = Product.query.filter_by(for_exchange=True).all()
    return render_template('home/exchange/products.html', products=products, manufacturer=manufacturer)


@home.route('/recycle/manufacturers/')
def show_recycle_manufacturers():
    manufacturers = Manufacturer.query.all()
    return render_template('home/recycle/manufacturers.html', manufacturers=manufacturers)


@home.route('/exchange/manufacturers/')
def show_exchange_manufacturers():
    manufacturers = Manufacturer.query.all()
    return render_template('home/exchange/manufacturers.html', manufacturers=manufacturers)


@home.route('/login/', methods=['GET', 'POST'])
def login():
    # 已登录用户则返回首页
    if g.user.is_authenticated():
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
