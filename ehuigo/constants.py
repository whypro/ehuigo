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
}


USER_STATUS = {
    'new': 0x00,  # 新注册，未激活
    #  已激活，正常用户
    'email_confirmed': 0x01,
    'cellphone_confirmed': 0x02,
    'frozen': 0x04,   # 被冻结
    'admin': 0x80  # 管理员
}


QUESTION_CATEGORY = {
    'recycle': 1,
    'exchange': 2,
}


QUESTION_CATEGORY_REVERSED = dict((v, k) for k, v in QUESTION_CATEGORY.items())


REG_EXP_PHONE = '^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$'
