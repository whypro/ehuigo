# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import current_app

from .uploader import LocalUploader


def create_uploader():
    uploader = LocalUploader()
    return uploader
