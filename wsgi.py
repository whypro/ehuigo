# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ehuigo import create_app
from ehuigo import config


app = create_app(config.Config)

