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
