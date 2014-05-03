#-*- coding: utf-8 -*-
import os
import re
import config

from app import db
from app import lib
from sqlalchemy.orm import validates

from datetime import datetime

EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')

class User(db.Model):
    __tablename__ = 'phantom_users'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('user_email', db.String(120), unique=True, nullable=False, index=True)
    password = db.Column('user_password', db.String(120), nullable=False)
    created_at = db.Column('user_created_at', db.DateTime, nullable=False)
    is_admin = db.Column('user_is_admin', db.Boolean)

    def __init__(self, email=None, password=None, is_admin=False):
        self.email = email
        self.password = lib.pw_hash(password)
        self.created_at = datetime.now()
        self.is_admin = is_admin

    @validates('email')
    def validates_email(self, key, email):
        assert EMAIL_REGEX.match(email)
        return email

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __unicode__(self):
        return '%r' % self.email


class Storage(db.Model):
    __tablename__ = 'phantom_storages'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('storage_name', db.String(64), nullable=False)
    path = db.Column('storage_path', db.String(512), nullable=False)
    tasks = db.relationship('Task', backref=db.backref('storage', cascade='all,delete'), lazy='dynamic')

    def __init__(self, name=name, path=path):
        self.name = name
        self.path = path

    @validates('path')
    def validates_path(self, key, path):
        assert os.access(path, os.W_OK)
        return os

    def __unicode__(self):
        return '%r' % (self.name)


class Task(db.Model):
    __tablename__ = 'phantom_tasks'
    id = db.Column('id', db.Integer, primary_key=True)
    storage_id = db.Column('storage', db.Integer, db.ForeignKey('phantom_storages.id'))
    name = db.Column('task_name', db.String(64), nullable=False)
    every_hour = db.Column('every_hour', db.Integer, nullable=False, index=True)
    max_stores = db.Column('task_max_stores', db.Integer, nullable=False, default=7)
    filename_rule = db.Column('task_filename_rule', db.String(32), nullable=True)
    results = db.relationship('TaskResult', backref=db.backref('task', cascade='all,delete'), lazy='dynamic')

    def __init__(self, storage, name, every_hour, max_stores, filename_rule):
        self.storage_id = storage.id if storage is not None else None
        self.name = name
        self.every_hour = every_hour
        self.max_stores = max_stores
        self.filename_rule = filename_rule

    @validates('every_hour')
    def validates_every_hour(self, key, hour):
        assert (hour.isdigit() and int(hour) >= 0 and int(hour) < 24)
        return int(hour)

    def __unicode__(self):
        return '%r' % (self.name)


class TaskResult(db.Model):
    __tablename__ = 'phantom_task_ressults'
    id = db.Column('id', db.Integer, primary_key=True)
    task_id = db.Column('task', db.Integer, db.ForeignKey('phantom_tasks.id'))
    result = db.Column('result', db.Boolean, default=False, index=True)
    executed_at = db.Column('result_executed_at', db.DateTime, nullable=False) # same as created_at
    completed_at = db.Column('result_completed_at', db.DateTime, nullable=True)

    def __init__(self, task):
        self.task_id = task.id if task is not None else None
        self.result = False
        self.executed_at = datetime.now()

    def __unicode__(self):
        pass

