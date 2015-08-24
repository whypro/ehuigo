# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort, current_app

from ..extensions import db
from ..models import Manufacturer, Product

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
def index():
    return render_template('admin/index.html')


@admin.route('/manufacturers/')
def show_manufacturers():
    return render_template('admin/manufacturers.html')


@admin.route('/products/')
def show_products():
    return render_template('admin/products.html')


@admin.route('/questions/')
def show_questions():
    return render_template('admin/questions.html')
