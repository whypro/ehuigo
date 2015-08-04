# -*- coding: utf-8 -*-
from . import create_app
from . import config


app = create_app(config.Config)

