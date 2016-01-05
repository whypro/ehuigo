# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from sqlalchemy import and_
from sqlalchemy.ext.associationproxy import association_proxy
from flask import current_app

from ..extensions import db
from ..constants import MAX_LENGTH, QUESTION_CATEGORY


class RecycleOrder(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(MAX_LENGTH['order_number']), unique=True, nullable=False)
    service_type = db.Column(db.Integer, nullable=False)
    fullname = db.Column(db.String(MAX_LENGTH['fullname']))
    cellphone = db.Column(db.String(MAX_LENGTH['cellphone']))
    address = db.Column(db.UnicodeText)
    zip_code = db.Column(db.String(MAX_LENGTH['zip_code']))
    remark = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User', passive_deletes=True)
    carrier = db.Column(db.String(MAX_LENGTH['carrier']))       # 快递公司
    tracking = db.Column(db.String(MAX_LENGTH['tracking']))     # 运单号
    status = db.Column(db.Integer)  # 订单状态
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)     # 创建时间
    send_time = db.Column(db.DateTime)       # 发货时间
    receive_time = db.Column(db.DateTime)    # 收货时间
    price = db.Column(db.Numeric(10, 2))    # 价格


class ExchangeOrder(object):
    pass


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(MAX_LENGTH['region_name']), nullable=False)
    name = db.Column(db.String(MAX_LENGTH['region_name']), nullable=False)
    parent_id = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    name_en = db.Column(db.String(MAX_LENGTH['region_name']), nullable=False)
    shortname_en = db.Column(db.String(MAX_LENGTH['region_name']), nullable=False)
