#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ehuigo import create_app

from config import config


app = create_app('ace')

application = app.wsgi_app
