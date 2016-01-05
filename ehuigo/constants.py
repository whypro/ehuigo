# -*- coding: utf-8 -*-
from __future__ import unicode_literals


MAX_LENGTH = {
    'email': 80,
    'username': 20,
    'password': 128,
    'cellphone': 20,
    'ip': 20,
    'path': 255,

    'manufacturer_name': 20,
    'product_model': 80,
    'product_version': 30,
    'question_content': 60,
    'question_remark': 120,
    'answer_content': 60,
    'answer_remark': 120,
    'category_name': 20,
    'fullname': 20,
    'region_name': 100,

    'order_number': 22,
    'zip_code': 10,
    'carrier': 20,
    'tracking': 20,
}


QUESTION_CATEGORY = {
    'recycle': 1,
    'exchange': 2,
}


QUESTION_CATEGORY_REVERSED = dict((v, k) for k, v in QUESTION_CATEGORY.items())


REG_EXP_PHONE = '^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$'


RECYCLE_ORDER_STATUS = {
    'created': 0,       # 用户创建
    'confirmed': 1,     # 商家确认
    'sent': 2,          # 用户发货
    'received': 3,      # 商家确认收货
    'accepted': 4,      # 商家评估通过
    'rejected': 5,      # 商家评估未通过
}
