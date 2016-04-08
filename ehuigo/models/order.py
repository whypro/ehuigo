# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from sqlalchemy import and_
from sqlalchemy.ext.associationproxy import association_proxy
from flask import current_app

from ..extensions import db
from ..constants import MAX_LENGTH, QUESTION_CATEGORY, RECYCLE_SERVICE_TYPE, RECYCLE_ORDER_STATUS_TYPE_OFFLINE, RECYCLE_ORDER_STATUS_TYPE_ONLINE


class RecycleOrder(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(MAX_LENGTH['order_number']), unique=True, nullable=False)
    service_type = db.Column(db.Integer, nullable=False)
    fullname = db.Column(db.String(MAX_LENGTH['fullname']))
    cellphone = db.Column(db.String(MAX_LENGTH['cellphone']))
    address = db.Column(db.UnicodeText)
    zip_code = db.Column(db.String(MAX_LENGTH['zip_code']))
    remark = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    user = db.relationship('User', passive_deletes=True)
    carrier = db.Column(db.String(MAX_LENGTH['carrier']))       # 快递公司
    tracking = db.Column(db.String(MAX_LENGTH['tracking']))     # 运单号
    state = db.Column(db.Integer, default=1)  # 订单状态
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)     # 创建时间
    send_time = db.Column(db.DateTime)       # 发货时间
    receive_time = db.Column(db.DateTime)    # 收货时间
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='SET NULL'))
    product = db.relationship('Product', passive_deletes=True)
    eval_detail = db.Column(db.Text)        # 估价详情
    eval_price = db.Column(db.Numeric(10, 2))     # 估价金额

    @staticmethod
    def _search_by_index(obj, index):
        for v1, v2, v3 in obj:
            if v1 == index:
                return v3
        return None

    def get_state(self):
        if self.state == 1:
            return self._search_by_index(RECYCLE_ORDER_STATUS_TYPE_OFFLINE, self.state)
        elif self.state == 2:
            return self._search_by_index(RECYCLE_ORDER_STATUS_TYPE_ONLINE, self.state)

    def get_service_type(self):
        return self._search_by_index(RECYCLE_SERVICE_TYPE, self.service_type)


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
