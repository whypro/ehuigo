#-*- coding:utf-8 -*-
from bae.core.wsgi import WSGIApplication

from ehuigo.wsgi import app


application = WSGIApplication(app)
