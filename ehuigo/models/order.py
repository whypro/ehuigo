# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy import and_
from sqlalchemy.ext.associationproxy import association_proxy
from flask import current_app

from ..extensions import db
from ..constants import MAX_LENGTH, QUESTION_CATEGORY


class RecycleOrder(object):
    pass


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
