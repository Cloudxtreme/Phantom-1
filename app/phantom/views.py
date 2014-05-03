#-*- coding: utf-* -*-
import json
import time

from app import db
from app import lib
from app import login_manager, login_required, logout_required, login_user, logout_user, current_user
from flask import Blueprint, Response, request, render_template, flash, g, session, redirect, url_for

from .models import User
from .forms import LoginForm

module = Blueprint('phantom', __name__)

@module.route('/', methods=['GET'])
def index():
    if User.query.count() == 0:
        return render_template('index_first.html')
    
    return render_template('index.html')

@module.route('/users/login', methods=['GET', 'POST'])
@logout_required
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.data['email']).first()
        login_user(user)
        return redirect(request.args.get('next') or '/')

    return render_template('user/login.html', form=form, login_url=url_for('.login'))
