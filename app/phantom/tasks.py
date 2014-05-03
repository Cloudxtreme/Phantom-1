#-*- coding: utf-8 -*-
from app import celery

@celery.task(name='tasks.phantom')
def phantom():
    pass