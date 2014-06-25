#-*- coding: utf-8 -*-
from datetime import datetime

from app import celery
from app import db

from .models import Task, TaskResult

@celery.task(name='tasks.phantom')
def phantom():
    now = datetime.now()
    today = now.date()
    now = (now.hour * 2) + (1 if now.minute > 30 else 0)

    tasks = []
    rules = Task.query.filter(Task.backup_time <= now)
    for rule in rules:
        if len(rule.results) > 0:
            if rule.results.executed_at.date() < today:
                tasks.append(rule)
        else:
            tasks.append(rule)

    for item in tasks:
        start_phantom.apply_async(item)

@celery.task(name='tasks.start_phantom')
def start_phantom(task):
    pass
