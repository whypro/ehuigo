# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import hashlib

from flask import current_app


class Uploader(object):

    class InvalidFileException(Exception):
        pass
    
    @staticmethod
    def _sha1(data):
        """
            根据文件生成 sha1 值
        """
        return hashlib.sha1(data).hexdigest()

    @staticmethod
    def _is_valid_ext(filename, allowed_list):
        return os.path.splitext(filename)[-1][1:].lower() in allowed_list

    @staticmethod
    def _is_valid_size(data):
        # print len(data)
        # print current_app.config['UPLOAD_MAX_SIZE']
        return len(data) < current_app.config['UPLOAD_MAX_SIZE']

    def save(self, file_storage):
        file_data = file_storage.read()
        if not self._is_valid_ext(file_storage.filename, current_app.config['UPLOAD_ALLOWED_EXT']) or not self._is_valid_size(file_data):
            raise InvalidFileException
        basename = self._sha1(file_data)
        ext = os.path.splitext(file_storage.filename)[-1]
        filename = basename + ext
        fullname = os.path.join(self.dirname, filename)
        self._store(fullname, file_data)
        return filename

    def _store(self, fullname, data):
        raise NotImplementedError

    def remove(self, filename):
        raise NotImplementedError


class LocalUploader(Uploader):
    
    def __init__(self):
        self.dirname = os.path.abspath(current_app.config['UPLOAD_PATH'])
        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)

    def _store(self, fullname, data):
        with open(fullname, 'wb') as f:
            f.write(data)

    def remove(self, filename):
        fullname = os.path.join(self.dirname, filename)
        try:
            os.remove(fullname)
        except OSError as e:
            print '文件不存在'
            # raise e

    # def url(self, filename):
    #     return '/' + current_app.config['UPLOAD_PREFIX'] + '/' + filename


class OSSUploader(Uploader):
    pass


if __name__ == '__main__':
    from werkzeug.datastructures import FileStorage
    fs = FileStorage(stream='test', filename='test.txt')
    # current_app.config = dict(UPLOAD_PATH='./uploads_test', IMAGE_EXT='txt', MAX_CONTENT_LENGTH=4*1024*1024)
    uploader = LocalUploader()
    uploader.save(fs)

