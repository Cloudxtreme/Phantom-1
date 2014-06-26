#-*- coding: utf-8 -*-
from datetime import datetime, timedelta
from json import dumps
import os
import random
from struct import unpack

import config
from flask.ext.bcrypt import Bcrypt
import md5 as md5module
import shortuuid

bcrypt = Bcrypt()
shortuuid.set_alphabet("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")

def md5(str):
    m = md5module.new()
    m.update(str)
    return m.hexdigest()

def make_token():
    return md5(shortuuid.uuid())

def pw_hash(plainpw):
    return bcrypt.generate_password_hash(plainpw)

def pw_verify(hashedpw, plainpw):
    return bcrypt.check_password_hash(hashedpw, plainpw)

def get_ext(fn):
    return os.path.splitext(fn)[1][1:]

def sizeof_fmt(num):
    for x in ['Bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.2f%s" % (num, x)
        num /= 1024.0
    return "%3.2f%s" % (num, 'TB')
