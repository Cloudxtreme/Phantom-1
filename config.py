#-*- coding: utf-8 -*-
from datetime import timedelta
import os

from celery.schedules import crontab

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = 'SecretKeyForSessionSigning'

if DEBUG is True:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://phantom:@localhost/phantom'
else:
    SQLALCHEMY_DATABASE_URI = ''
DATABASE_CONNECT_OPTIONS = {}

# celery run with `celery -A app.celery worker -B` (with celerybeat)
CELERY_IMPORTS = (
    'app.phantom.tasks',
)
CELERY_BROKER_URL = 'redis://localhost:6379' # or your broker of choice.
CELERY_TIMEZONE = 'Asia/Seoul' # or set your timezone.
CELERYBEAT_SCHEDULE = {
    'phantom': {
        'task': 'tasks.phantom',
        'schedule': timedelta(minutes=30),
        'args': (),
    },
}

CSRF_ENABLED = True
CSRF_SESSION_KEY = "somethingimpossibletoguess"

