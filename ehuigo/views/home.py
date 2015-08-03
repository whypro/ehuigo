# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort, current_app

from ..extensions import db
from ..models import Manufacturer, Product

home = Blueprint('home', __name__)


@home.route('/')
def index():
    manufacturers = Manufacturer.query.all()
    hot_products = Product.query.order_by(Product.price.desc()).limit(current_app.config['HOT_PRODUCT_NUM']).all()
    return render_template('index.html', manufacturers=manufacturers, hot_products=hot_products)


@home.route('/eval/<int:id>/')
def eval(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('eval.html', product=product)


@home.route('/init/')
def init():
    db.create_all()
    return redirect(url_for('home.index'))
