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

    ORDER_STATE_CREATED = 1
    ORDER_STATE_SENT = 2
    ORDER_STATE_RECEIVED = 3
    ORDER_STATE_CONFIRMED = 4
    ORDER_STATE_VISITING = 5
    ORDER_STATE_ACCEPTED = 6
    ORDER_STATE_REJECTED = 7

    SERVICE_TYPE_OFFLINE = 1
    SERVICE_TYPE_ONLINE = 2

    def can_send(self):
        if self.service_type == self.SERVICE_TYPE_ONLINE:
            if self.state == self.ORDER_STATE_CREATED:
                return True
        return False

    def send(self, tracking, carrier):
        if self.service_type == self.SERVICE_TYPE_ONLINE:
            if self.state == self.ORDER_STATE_CREATED:
                current_app.logger.debug('Order {0} state: CREATED -> SENT'.format(self.id))
                self.tracking = tracking
                self.carrier = carrier
                self.send_time = datetime.datetime.now()
                self.state = self.ORDER_STATE_SENT
                return 0
        return -1

    def can_receive(self):
        if self.service_type == self.SERVICE_TYPE_ONLINE:
            if self.state == self.ORDER_STATE_SENT:
                return True
        return False

    def receive(self):
        if self.service_type == self.SERVICE_TYPE_ONLINE:
            if self.state == self.ORDER_STATE_SENT:
                current_app.logger.debug('Order {0} state: SENT -> RECEIVED'.format(self.id))
                self.receive_time = datetime.datetime.now()
                self.state = self.ORDER_STATE_RECEIVED
                return 0
        return -1

    def can_confirm(self):
        if self.service_type == self.SERVICE_TYPE_OFFLINE:
            if self.state == self.ORDER_STATE_CREATED:
                return True
        return False

    def confirm(self):
        if self.service_type == self.SERVICE_TYPE_OFFLINE:
            if self.state == self.ORDER_STATE_CREATED:
                current_app.logger.debug('Order {0} state: CREATED -> CONFIRMED'.format(self.id))
                self.state = self.ORDER_STATE_CONFIRMED
                return 0
        return -1

    def visit(self):
        if self.service_type == self.SERVICE_TYPE_OFFLINE:
            if self.state == self.ORDER_STATE_CONFIRMED:
                current_app.logger.debug('Order {0} state: CONFIRMED -> VISITING'.format(self.id))
                self.state = self.ORDER_STATE_VISITING
                return 0
        return -1

    def accept(self):
        if self.service_type == self.SERVICE_TYPE_OFFLINE:
            if self.state == self.ORDER_STATE_VISITING:
                current_app.logger.debug('Order {0} state: VISITING -> ACCEPTED'.format(self.id))
                self.state = self.ORDER_STATE_ACCEPTED
                return 0
        elif self.service_type == self.SERVICE_TYPE_ONLINE:
            if self.state == self.ORDER_STATE_RECEIVED:
                current_app.logger.debug('Order {0} state: RECEIVED -> ACCEPTED'.format(self.id))
                self.state = self.ORDER_STATE_ACCEPTED
                return 0
        return -1

    def reject(self):
        if self.service_type == self.SERVICE_TYPE_OFFLINE:
            if self.state == self.ORDER_STATE_CREATED:
                current_app.logger.debug('Order {0} state: CREATED -> REJECTED'.format(self.id))
                self.state = self.ORDER_STATE_REJECTED
                return 0
        elif self.service_type == self.SERVICE_TYPE_ONLINE:
            if self.state == self.ORDER_STATE_RECEIVED:
                current_app.logger.debug('Order {0} state: RECEIVED -> REJECTED'.format(self.id))
                self.state = self.ORDER_STATE_REJECTED
                return 0
        return -1

    def get_order_state(self):
        if self.state == self.ORDER_STATE_CREATED:
            if self.service_type == self.SERVICE_TYPE_OFFLINE:
                return '待确认'
            elif self.service_type == self.SERVICE_TYPE_ONLINE:
                return '待邮寄'
        elif self.state == self.ORDER_STATE_SENT:
            return '已邮寄'
        elif self.state == self.ORDER_STATE_RECEIVED:
            return '已收件'
        elif self.state == self.ORDER_STATE_CONFIRMED:
            return '已确认'
        elif self.state == self.ORDER_STATE_VISITING:
            return '上门取货中'
        elif self.state == self.ORDER_STATE_ACCEPTED:
            return '如实描述'
        elif self.state == self.ORDER_STATE_REJECTED:
            return '描述不符'

    def get_service_type(self):
        if self.service_type == self.SERVICE_TYPE_OFFLINE:
            return '上门服务'
        elif self.service_type == self.SERVICE_TYPE_ONLINE:
            return '邮寄服务'



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


class Carrier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_LENGTH['carrier']), nullable=False)

