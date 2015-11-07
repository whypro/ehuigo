# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib

from ..models import Manufacturer, Question, Answer, Product, User, Price


def init_manufacturers_and_products(session):
    m = Manufacturer(name='苹果', alias='APPLE', logo='/static/images/manufacturers/apple.png')
    session.add(m)
    p = Product(manufacturer=m, model='iPhone 6', version='', photo='/static/images/products/iPhone6.jpg')
    session.add(p)
    p = Product(manufacturer=m, model='iPhone 6 Plus', version='', photo='/static/images/products/iPhone6p.jpg')
    session.add(p)
    p = Product(manufacturer=m, model='iPhone 5s', version='', photo='/static/images/products/iPhone5s.jpg')
    session.add(p)
    p = Product(manufacturer=m, model='iPhone 5c', version='', photo='/static/images/products/iPhone5c.jpg')
    session.add(p)

    m = Manufacturer(name='HTC', alias=None, logo='/static/images/manufacturers/htc.png')
    session.add(m)
    m = Manufacturer(name='华为', alias='HUAWEI', logo='/static/images/manufacturers/huawei.png')
    session.add(m)
    m = Manufacturer(name='诺基亚', alias='NOKIA', logo='/static/images/manufacturers/nokia.png')
    session.add(m)
    m = Manufacturer(name='三星', alias='SAMSUNG', logo='/static/images/manufacturers/samsung.png')
    session.add(m)
    m = Manufacturer(name='小米', alias=None, logo='/static/images/manufacturers/xiaomi.png')
    session.add(m)
    m = Manufacturer(name='魅族', alias='MEIZU', logo='/static/images/manufacturers/xiaomi.png')
    session.add(m)
    m = Manufacturer(name='联想', alias='LENOVE', logo='/static/images/manufacturers/lenovo.png')
    session.add(m)

    session.commit()


def init_questions_and_answers(session):
    q = Question(content='开关机情况')
    session.add(q)
    a = Answer(question=q, content='能开机')
    session.add(a)
    a = Answer(question=q, content='不能开机')
    session.add(a)

    q = Question(content='维修拆机情况')
    session.add(q)
    a = Answer(question=q, content='无拆机')
    session.add(a)
    a = Answer(question=q, content='有拆机')
    session.add(a)

    q = Question(content='进液情况')
    session.add(q)
    a = Answer(question=q, content='无进水')
    session.add(a)
    a = Answer(question=q, content='有进水')
    session.add(a)

    q = Question(content='外观成色')
    session.add(q)
    a = Answer(question=q, content='全新')
    session.add(a)
    a = Answer(question=q, content='外观完好')
    session.add(a)
    a = Answer(question=q, content='有磕碰')
    session.add(a)

    q = Question(content='触摸屏情况')
    session.add(q)
    a = Answer(question=q, content='正常')
    session.add(a)
    a = Answer(question=q, content='失效')
    session.add(a)

    q = Question(content='显示屏情况')
    session.add(q)
    a = Answer(question=q, content='正常')
    session.add(a)
    a = Answer(question=q, content='有色差')
    session.add(a)

    q = Question(content='配件情况')
    session.add(q)
    a = Answer(question=q, content='全套配件')
    session.add(a)
    a = Answer(question=q, content='配件不全')
    session.add(a)
    a = Answer(question=q, content='无配件')
    session.add(a)

    session.commit()


def init_user(session, email, password, nickname):
    u = User(
        email=email, 
        password=hashlib.sha1(password).hexdigest(), 
        nickname=nickname
    )
    session.add(u)
    session.commit()
