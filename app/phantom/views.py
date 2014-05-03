#-*- coding: utf-* -*-
import json
import time

from app import db
from app import lib
from app import login_manager, login_required, logout_required, login_user, logout_user, current_user
from flask import Blueprint, Response, request, render_template, flash, g, session, redirect, url_for, abort

from .models import User
from .forms import LoginForm, RegisterForm

module = Blueprint('phantom', __name__)

@module.route('/', methods=['GET'])
def index():
    if User.query.count() == 0:
        form = RegisterForm()
        return render_template('index_first.html', form=form)
    elif not current_user.is_authenticated():
        form = LoginForm()
        return render_template('user/login.html', form=form, login_url=url_for('.login'))

    return render_template('index.html')

@module.route('/user/register', methods=['POST'])
@logout_required
def register():
    if User.query.count() > 0:
        abort(403)

    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        user = User(form.data['email'], form.data['password'], True)
        db.session.add(user)
        db.session.commit()
        if user:
            flash('created your account. please sign in.')
            return redirect('/')

    return render_template('index_first.html', form=form)

@module.route('/user/login', methods=['POST'])
@logout_required
def login():
    form = LoginForm()
    if form.validate():
        user = User.query.filter_by(email=form.data['email']).first()
        login_user(user)
        return redirect(request.args.get('next') or '/')

    return render_template('user/login.html', form=form, login_url=url_for('.login'))

@module.route('/user/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')