# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from threading import Thread
from smtplib import SMTPServerDisconnected
from ssl import SSLError
import time

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


def _async_send_email(app, msg, retry=3):
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
    thread = Thread(target=_async_send_email, args=[current_app._get_current_object(), msg])
    thread.start()
    return thread
    # mail.send(msg)


def get_client_ip():
    # 获取 ip 地址
    if 'x-forwarded-for' in request.headers:
        ip = request.headers['x-forwarded-for'].split(', ')[0]
    else:
        ip = request.remote_addr
    return ip
