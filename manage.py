#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ehuigo import create_app
from ehuigo import config

from flask.ext.script import Manager, Server
# from flask.ext.migrate import Migrate, MigrateCommand


app = create_app(config.Config)

# migrate = Migrate(app, db)

manager = Manager(app)
# manager.add_command('db', MigrateCommand)
# manager.add_command('debug', Server(host='127.0.0.1', port=8080, debug=True))

@manager.command
def debug():
    """Start Server in debug mode"""
    app.run(host='0.0.0.0', port=5000, debug=True, processes=1)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, processes=10, debug=True)
    # app.run(host='0.0.0.0', port=8080, debug=True)
    manager.run()
