# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Blueprint, render_template, request, jsonify, redirect, abort, current_app, send_from_directory
from sqlalchemy.sql import func
from sqlalchemy import or_

from ..models import Manufacturer, Product


home = Blueprint('home', __name__)


@home.route('/')
def index():
    manufacturers = Manufacturer.query.limit(current_app.config['HOT_MANUFACTURER_NUM']).all()
    hot_products = Product.query.filter_by(for_recycle=True).limit(current_app.config['HOT_PRODUCT_NUM']).all()
    return render_template('index.html', manufacturers=manufacturers, hot_products=hot_products)


@home.route('/recycle/product/<int:product_id>/')
def show_recycle_product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    if not product.for_recycle:
        abort(404)
    return render_template('home/recycle/product_detail.html', product=product)


@home.route('/exchange/product/<int:product_id>/')
def show_exchange_product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    if not product.for_exchange:
        abort(404)
    return render_template('home/exchange/product_detail.html', product=product)


@home.route('/uploads/<filename>')
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


@home.route('/recycle/search/', methods=['POST'])
def search_products():
    key = request.form.get('key')
    if not key:
        abort(400)
    search_string = '%{key}%'.format(key=key)
    products_1 = Product.query.filter(Product.model.like(search_string), Product.for_recycle==True)
    subqry = Manufacturer.query.filter(or_(Manufacturer.name.like(search_string), Manufacturer.alias.like(search_string))).subquery()
    products_2 = Product.query.filter(Product.manufacturer_id==subqry.c.id, Product.for_recycle==True)
    products = products_1.union(products_2).all()
    
    return render_template('home/recycle/products_search.html', products=products, key=key)


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
    subqry = Product.query.group_by(Product.manufacturer_id).having(func.bit_or(Product.for_recycle)!=False).subquery()
    # print subqry
    manufacturers = Manufacturer.query.join(subqry, Manufacturer.id==subqry.c.manufacturer_id).all()
    return render_template('home/recycle/manufacturers.html', manufacturers=manufacturers)


@home.route('/exchange/manufacturers/')
def show_exchange_manufacturers():
    subqry = Product.query.group_by(Product.manufacturer_id).having(func.bit_or(Product.for_exchange)!=False).subquery()
    # print subqry
    manufacturers = Manufacturer.query.join(subqry, Manufacturer.id==subqry.c.manufacturer_id).all()
    return render_template('home/exchange/manufacturers.html', manufacturers=manufacturers)


@home.route('/400/')
def test_error_400():
    abort(400)


@home.route('/404/')
def test_error_404():
    abort(404)


@home.route('/500/')
def test_error_500():
    abort(500)
