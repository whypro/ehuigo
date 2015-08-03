#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import subprocess

from flask.ext.script import Manager, Server
from flask.ext.migrate import  MigrateCommand

from ehuigo import create_app
from ehuigo import config
from ehuigo.extensions import db



app = create_app(config.Config)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
# manager.add_command('debug', Server(host='127.0.0.1', port=8080, debug=True))

@manager.command
def debug():
    """Start Server in debug mode"""
    app.run(host='0.0.0.0', port=5000, debug=True, processes=1)


@manager.command
def init():
    # 创建数据库
    create_db_sql = 'CREATE DATABASE IF NOT EXISTS {0} DEFAULT CHARACTER SET utf8'.format(config.Config.DB_DATABASE)
    # print create_db_sql
    ret = subprocess.call(
        [
            'mysql', '-u', config.Config.DB_USERNAME,
            '-p{0}'.format(config.Config.DB_PASSWORD),
            '-e', create_db_sql,
        ]
    )
    if not ret:
        print '数据库创建成功'
    else:
        print '数据库创建失败'
        return 

    db.drop_all()
    db.create_all()
    print '数据表创建成功'
    # init_home(db.session)
    # init_post(db.session)
    # init_member(db.session)
    # print '数据初始化成功'


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, processes=10, debug=True)
    # app.run(host='0.0.0.0', port=8080, debug=True)
    manager.run()
