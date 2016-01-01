# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import io

from flask import Blueprint, render_template, request, jsonify, redirect, abort, current_app, send_from_directory, send_file, session, url_for
from sqlalchemy.sql import func
from sqlalchemy import or_
from captcha.image import ImageCaptcha

from ..models import Region
from ..helpers import send_sms, gen_captcha_str
from ..captcha import create_captcha
from ..forms import RecycleOrderForm


order = Blueprint('order', __name__, url_prefix='/order')


@order.route('/add/', methods=['GET', 'POST'])
def add_order():
    form = RecycleOrderForm()
    if form.province.data == 0: form.province.data = None
    if form.city.data == 0: form.city.data = None
    if form.county.data == 0: form.county.data = None
    # 从数据库中动态获取选项
    provinces = Region.query.filter_by(parent_id=1).all()
    cities = Region.query.filter_by(parent_id=form.province.data).all()
    counties = Region.query.filter_by(parent_id=form.city.data).all()
    form.province.choices = [(0, '请选择省份')] + [(p.id, p.name) for p in provinces]
    form.city.choices = [(0, '请选择城市')] + [(c.id, c.name) for c in cities]
    form.county.choices = [(0, '请选择县区')] + [(c.id, c.name) for c in counties]

    if form.validate_on_submit():
        return redirect(url_for('order.add_order'))
    return render_template('order/order_add.html', form=form)
