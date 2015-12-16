# -*- coding: utf-8 -*-
from __future__ import unicode_literals


MAX_LENGTH = {
    'email': 80,
    'username': 20,
    'password': 128,
    'mobile': 20,
    'ip': 20,
    'path': 255,

    'manufacturer_name': 20,
    'product_model': 80,
    'product_version': 30,
    'question_content': 60,
    'question_remark': 120,
    'answer_content': 60,
    'answer_remark': 120,
}


USER_STATUS = {
    'active': 0,   # 已激活，正常用户
    'new': 1,      # 新注册，未激活
    'frozen': 2,   # 被冻结
}
