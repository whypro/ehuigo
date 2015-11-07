# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .uploader import LocalUploader


def create_uploader():
    uploader = LocalUploader()
    return uploader
