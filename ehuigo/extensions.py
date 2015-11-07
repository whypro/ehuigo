# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate

db = SQLAlchemy()

migrate = Migrate()

