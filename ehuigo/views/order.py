# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import io
import datetime

from flask import Blueprint, render_template, request, jsonify, redirect, abort, current_app, send_from_directory, send_file, session, url_for, flash
from flask.ext.login import current_user, login_required
from sqlalchemy.sql import func
from sqlalchemy import or_
from captcha.image import ImageCaptcha

from ..models import Region, RecycleOrder
from ..helpers import send_sms, gen_captcha_str, gen_order_number
from ..captcha import create_captcha
from ..forms import RecycleOrderForm, TrackingAddForm
from ..extensions import db


order = Blueprint('order', __name__, url_prefix='/order')


@order.route('/add/', methods=['GET', 'POST'])
@login_required
def add_order():
    if 'recycle' not in session:
        flash('页面已过期，请重新进行估价', 'danger')
        current_app.logger.error('Key recycle is not in app session')
        return redirect(url_for('home.index'))

    recycle_data = session['recycle']

    # 初始化 form
    form = RecycleOrderForm(fullname=current_user.fullname, cellphone=current_user.cellphone)
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
        province = Region.query.get(form.province.data)
        city = Region.query.get(form.city.data)
        county = Region.query.get(form.county.data)
        recycle_order = RecycleOrder(
            order_number=gen_order_number(),
            service_type=form.service_type.data,
            remark=form.remark.data,
            user_id=current_user.id,
            fullname=form.fullname.data,
            cellphone=form.cellphone.data,
            address=province.name+city.name+county.name+form.address.data,
            eval_detail=recycle_data['detail'],
            eval_price=recycle_data['price'],
            product_id=recycle_data['product_id']
        )
        db.session.add(recycle_order)
        db.session.commit()
        session.pop('recycle')
        flash('订单创建成功', 'success')
        return redirect(url_for('order.show_orders'))

    return render_template(
        'order/order_add.html', form=form,
        product_id=recycle_data['product_id'], price=recycle_data['price'], detail=recycle_data['detail']
    )


@order.route('/orders/')
@login_required
def show_orders():
    orders = RecycleOrder.query.filter_by(user_id=current_user.id)
    return render_template('order/orders.html', orders=orders)


@order.route('/<int:order_id>/')
@login_required
def show_order_detail(order_id):
    order_ = RecycleOrder.query.get_or_404(order_id)
    if order_.user_id != current_user.id:
        abort(403)
    # return str(order_id)
    return render_template('order/order_detail.html', order=order_)


@order.route('/<int:order_id>/tracking/add/', methods=['GET', 'POST'])
@login_required
def add_tracking(order_id):
    order_ = RecycleOrder.query.get_or_404(order_id)
    if order_.user_id != current_user.id:
        abort(403)

    if not order_.can_send():
        abort(400)

    form = TrackingAddForm()
    # print form.carrier.choices
    if form.validate_on_submit():
        # print form.tracking.data
        # print form.carrier.data
        order_.send(tracking=form.tracking.data, carrier=form.carrier.data)
        db.session.add(order_)
        db.session.commit()

        return redirect(url_for('order.show_order_detail', order_id=order_.id))

    return render_template('order/tracking_add.html', form=form, order=order_)


@order.route('/<int:order_id>/cancel/')
@login_required
def cancel_order(order_id):
    order = RecycleOrder.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        abort(403)
    if not order.can_cancel():
        abort(400)

    order.cancel()
    db.session.add(order)
    db.session.commit()
    return redirect(url_for('order.show_order_detail', order_id=order.id))