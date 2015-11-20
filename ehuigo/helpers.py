# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import current_app

from .uploader import LocalUploader, OSSUploader


def create_uploader():
    if 'OSS_ENDPOINT' in current_app.config:
        uploader = OSSUploader()
    else:
        uploader = LocalUploader()
    return uploader


def get_object_fullname(filename):
    if 'OSS_ENDPOINT' in current_app.config:
        prefix = 'http://' + current_app.config['OSS_ENDPOINT']
    else:
        prefix = current_app.config['UPLOAD_PATH']
    return prefix + '/' + filename
