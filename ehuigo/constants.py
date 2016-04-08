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


RECYCLE_SERVICE_TYPE = (
    (1, 'offline', '上门服务'),
    (2, 'online', '邮寄服务'),
)

RECYCLE_ORDER_STATUS_TYPE_OFFLINE = (
    (1, 'created', '待确认'),
    (2, 'confirmed', '已确认'),
    (3, 'coming', '上门取货中'),
    (4, 'accepted', '如实描述'),
    (5, 'rejected', '描述不符'),
)

RECYCLE_ORDER_STATUS_TYPE_ONLINE = (
    (1, 'created', '待邮寄'),
    (2, 'sent', '已邮寄'),
    (3, 'received', '已收件'),
    (4, 'accepted', '如实描述'),
    (5, 'rejected', '描述不符'),
)

