#-*- coding: utf-8 -*-
import config

from app import lib
from .models import User

from flask_wtf import Form
from wtforms import TextField, PasswordField
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
        elif not lib.pw_verify(user.password, self.password.data):
            self.password.errors.append('Password not match')
            return False
        else:
            return True


