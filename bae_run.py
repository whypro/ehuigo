#-*- coding:utf-8 -*-
from bae.core.wsgi import WSGIApplication

from ehuigo import create_app
from ehuigo import config


app = create_app(config.BAEConfig)

application = WSGIApplication(app)
