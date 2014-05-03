#-*- coding: utf-8 -*-
import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = 'SecretKeyForSessionSigning'

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
if DEBUG is True:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://phantom:phantom@localhost/phantom'
else:
    SQLALCHEMY_DATABASE_URI = ''
DATABASE_CONNECT_OPTIONS = {}

CSRF_ENABLED = True
CSRF_SESSION_KEY = "somethingimpossibletoguess"
