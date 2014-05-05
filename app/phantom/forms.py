#-*- coding: utf-8 -*-
import os
import config

from app import lib
from .models import User, Storage

from flask_wtf import Form
from wtforms import TextField, PasswordField, IntegerField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import validators as v

class LoginForm(Form):
    email = TextField('email', validators=[ v.Email(), v.DataRequired() ])
    password = PasswordField('password', validators=[ v.DataRequired() ])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            self.email.errors.append('User not exists')
            return False
        elif not user.check_password(self.password.data):
            self.password.errors.append('Password not match')
            return False
        else:
            return True


class RegisterForm(Form):
    email = TextField('Email', validators=[ v.Email(), v.DataRequired(), v.length(max=120) ])
    password = PasswordField('Password', validators=[ v.DataRequired() ])
    password_check = PasswordField('Confirm password', validators=[ v.DataRequired() ])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if len(self.password.data) < 6:
            self.password.erros.append('Password is too short (Minimum password length is 6)')
            return False

        if self.password.data != self.password_check.data:
            self.password_check.errors.append('Password check is not match')
            return False

        return True

class AddStorageForm(Form):
    name = TextField('Name', validators=[ v.DataRequired(), v.length(max=64) ])
    path = TextField('Path', validators=[ v.DataRequired(), v.length(max=512) ])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if len(self.path.data) > 0 and not self.path.data.startswith('/'):
            self.path.errors.append('Target path must start with "/" (absolute path)')
            return False

        if not os.path.isdir(self.path.data):
            self.path.errors.append('Target path is not directory')
            return False

        if not os.access(self.path.data, os.W_OK):
            self.path.errors.append('Target path is not writable')
            return False

        return True

class AddTaskForm(Form):
    '''
    TIME FORMAT
    0 -> 00:00, 1 -> 00:30, 2 -> 01:00 .. 47 -> 23:30
    '''
    TIME_CHOICES = [(i, '%.2d:%.2d' % (time / 2, 30 if time % 2 is 1 else 0))
                            for i, time in enumerate([t for t in range(0, 48)])]

    name = TextField('Name', validators=[ v.DataRequired(), v.length(max=64) ])
    storage = QuerySelectField(query_factory=Storage.query.all,
                                    get_pk=lambda o: o.id,
                                    get_label=lambda o: o.name)
    backup_path = TextField('Backup Path', validators=[ v.DataRequired(), v.length(max=512) ])
    backup_time = SelectField('Backup time', coerce=int, choices=TIME_CHOICES, validators=[ v.NumberRange(min=0, max=47) ])
    max_stores = IntegerField('Max file stores (days)', validators=[ v.DataRequired(), v.NumberRange(min=1) ], default=7)
    filename_rule = TextField('Filename Rule', validators=[ v.DataRequired() ], default='{NAME}_{DATE}{TIME}')

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if len(self.backup_path.data) > 0 and not self.backup_path.data.startswith('/'):
            self.backup_path.errors.append('Backup path must start with "/" (absolute path)')
            return False

        if not os.path.isdir(self.backup_path.data):
            self.backup_path.errors.append('Backup path is not directory')
            return False

        return True
