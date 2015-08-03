# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort, current_app

from ..extensions import db
from ..models import Manufacturer, Product

home = Blueprint('home', __name__)


@home.route('/')
def index():
    manufacturers = Manufacturer.query.limit(current_app.config['HOT_MANUFACTURER_NUM']).all()
    hot_products = Product.query.order_by(Product.price.desc()).limit(current_app.config['HOT_PRODUCT_NUM']).all()
    return render_template('index.html', manufacturers=manufacturers, hot_products=hot_products)


@home.route('/eval/<int:product_id>/')
def show_evaluation(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('eval.html', product=product)


@home.route('/eval/', methods=['POST'])
def evaluate():
    return redirect('home.index')


@home.route('/init/')
def init():
    db.create_all()
    return redirect(url_for('home.index'))
