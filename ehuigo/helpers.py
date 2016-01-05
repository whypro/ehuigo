# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from threading import Thread
from urlparse import urljoin
import datetime
import hashlib
import base64
import urllib
import urllib2
import json
import string
import random
import datetime

from flask import current_app, render_template, request
from flask.ext.mail import Message

from .uploader import LocalUploader, OSSUploader
from .extensions import mail


def create_uploader():
    if 'OSS_ENDPOINT' in current_app.config:
        uploader = OSSUploader()
    else:
        uploader = LocalUploader()
    return uploader


# 有 BUG
def _async_send_email(app, msg, retry=3):
    from smtplib import SMTPServerDisconnected
    from ssl import SSLError
    import time
    with app.app_context():
        for i in range(retry):
            try:
                mail.send(msg)
            except SSLError as e:
                app.logger.error(e)
            except SMTPServerDisconnected as e:
                app.logger.error(e)
            else:
                break
            time.sleep(1)


def send_email(to, subject, template, **kwargs):
    msg = Message(subject=subject, sender=current_app.config['EHUIGO_MAIL_SENDER'], recipients=[to])
    msg.html = render_template(template, **kwargs)
    # thread = Thread(target=_async_send_email, args=[current_app._get_current_object(), msg])
    # thread.start()
    # return thread
    mail.send(msg)


def send_sms(to, template_id, template_data):
    """
        REST API 验证参数，生成规则如下
        1.使用MD5加密（账户Id + 账户授权令牌 + 时间戳）。其中账户Id和账户授权令牌根据url的验证级别对应主账户。时间戳是当前系统时间，格式"yyyyMMddHHmmss"。时间戳有效时间为24小时，如：20140416142030
        2.SigParameter参数需要大写，如不能写成sig=abcdefg而应该写成sig=ABCDEFG
    """
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    sig_parameter = hashlib.md5(
        current_app.config['YUNTONGXUN_ACCOUNT_SID'] +
        current_app.config['YUNTONGXUN_AUTH_TOKEN'] +
        timestamp
    ).hexdigest().upper()
    path = '/2013-12-26/Accounts/{accountSid}/SMS/TemplateSMS?sig={SigParameter}'.format(
        accountSid=current_app.config['YUNTONGXUN_ACCOUNT_SID'],
        SigParameter=sig_parameter
    )
    url = urljoin(current_app.config['YUNTONGXUN_BASE_URL'], path)
    print url

    # to 必选 短信接收端手机号码集合，用英文逗号分开，每批发送的手机号数量不得超过100个
    # appId 必选	应用Id
    # templateId 必选 模板Id
    # datas 必选 内容数据外层节点
    data = {
        'to': ','.join(to),
        'appId': current_app.config['YUNTONGXUN_APP_ID'],
        'templateId': template_id,
        'datas': template_data
    }
    json_data = json.dumps(data)
    print json_data

    # Authorization:
    # 1.使用Base64编码（账户Id + 冒号 + 时间戳）其中账户Id根据url的验证级别对应主账户
    # 2.冒号为英文冒号
    # 3.时间戳是当前系统时间，格式"yyyyMMddHHmmss"，需与SigParameter中时间戳相同。
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=utf-8',
        'Content-Length': len(json_data),
        'Authorization': base64.b64encode('{accountSid}:{timestamp}'.format(accountSid=current_app.config['YUNTONGXUN_ACCOUNT_SID'], timestamp=timestamp))
    }

    req = urllib2.Request(url, data=json_data, headers=headers)
    resp = urllib2.urlopen(req)
    return json.loads(resp.read())


def get_client_ip():
    # 获取 ip 地址
    if 'x-forwarded-for' in request.headers:
        ip = request.headers['x-forwarded-for'].split(', ')[0]
    else:
        ip = request.remote_addr
    return ip


def gen_captcha_str(length, digits_only=False):
    characters = string.digits
    if not digits_only:
        characters += string.letters
    characters = filter(lambda x: x not in 'IloO01', characters)
    result = random.sample(characters, length)
    return ''.join(result)


def gen_order_number():
    # 格式：20160104181823411000
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3] + unicode(random.randint(0, 999)).rjust(3, '0')
