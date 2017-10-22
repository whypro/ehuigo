#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import subprocess
import datetime
import shutil
import os
from zipfile import ZipFile

from flask.ext.script import Manager, Server, Shell
from flask.ext.migrate import  MigrateCommand

from ehuigo import create_app
from ehuigo.extensions import db
from ehuigo.scripts.init_data import init_manufacturers_and_products, init_questions_and_answers, init_user

from config import config


# 覆盖检测
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='ehuigo/*')
    COV.start()

config_name = 'development'

app = create_app(config_name)


def _make_shell_context():
    from ehuigo.models import User
    return dict(app=app, db=db, User=User)


manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=_make_shell_context))
# manager.add_command('debug', Server(host='127.0.0.1', port=8080, debug=True))


@manager.command
def debug():
    """Start Server in debug mode"""
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=False, processes=1)


@manager.command
def init():
    # 创建数据库
    create_db_sql = 'CREATE DATABASE IF NOT EXISTS {0} DEFAULT CHARACTER SET utf8'.format(config[config_name].DB_DATABASE)
    # print create_db_sql
    ret = subprocess.call(
        [
            'mysql', '-u', config[config_name].DB_USERNAME,
            '-p{0}'.format(config[config_name].DB_PASSWORD),
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
    init_manufacturers_and_products(db.session)
    init_questions_and_answers(db.session)
    # init_home(db.session)
    # init_post(db.session)
    # init_member(db.session)
    # print '数据初始化成功'
    print '请输入管理员邮箱：'
    email = raw_input()
    print '请输入管理员密码：'
    password = raw_input()
    print '请输入管理员昵称：'
    nickname = raw_input()
    init_user(db.session, email, password, nickname)
    print '管理员账户初始化成功'


@manager.command
def backup():
    # 备份上传文件
    date_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    ret = shutil.make_archive('backup/uploads-{date}'.format(date=date_str), 'zip', './', 'uploads')
    print '文件已备份至 {0}'.format(ret)
    # print ret

    # 备份数据库
    sql_file = 'backup/ehuigo-{date}.sql'.format(date=date_str)
    f = open(sql_file, 'w')
    ret = subprocess.call(
        [
            'mysqldump', '-u', config[config_name].DB_USERNAME,
            '-p{0}'.format(config[config_name].DB_PASSWORD),
            config[config_name].DB_DATABASE,
        ],
        stdout=f
    )
    f.close()
    if not ret:
        print '数据库已备份至 {0}'.format(os.path.abspath(sql_file))
    else:
        os.remove(sql_file)
        print '数据库备份失败'


@manager.command
def restore():
    files = os.listdir('backup')
    print '可以还原的备份文件有：'
    print '\n'.join(set([bf.split('-')[-1].split('.')[0] for bf in files]))
    print '请选择备份文件日期：'
    date_str = raw_input()

    # 还原数据库
    f = open('backup/ehuigo-{date}.sql'.format(date=date_str), 'r')
    ret = subprocess.call(
        [
            'mysql', '-u', config[config_name].DB_USERNAME,
            '-p{0}'.format(config[config_name].DB_PASSWORD),
            config[config_name].DB_DATABASE,
        ],
        stdin=f
    )
    f.close()
    if not ret:
        print '数据库已还原'
    else:
        print '数据库还原失败'

    # 还原上传文件
    with ZipFile('backup/uploads-{date}.zip'.format(date=date_str), 'r') as z:
        z.extractall()
    print '文件已还原'


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable]+sys.argv)

    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

    if COV:
        COV.stop()
        COV.save()
        print 'Coverage Summary:'
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print 'HTML version: file://{0}/index.html'.format(covdir)
        COV.erase()


@manager.command
def profile(length=25, profile_dir='tmp/profiler'):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length], profile_dir=profile_dir)
    app.run()


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, processes=10, debug=True)
    # app.run(host='0.0.0.0', port=8080, debug=True)
    manager.run()
