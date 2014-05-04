#-*- coding: utf-* -*-
import json
import time

from app import db
from app import lib
from app import csrf
from app import login_manager, login_required, logout_required, login_user, logout_user, current_user
from flask import Blueprint, Response, request, render_template, flash, g, session, redirect, url_for, abort, jsonify

from .models import User, Storage, Task, TaskResult
from .forms import LoginForm, RegisterForm, AddStorageForm

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

@module.route('/users/register', methods=['POST'])
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

@module.route('/users/login', methods=['POST'])
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

@csrf.exempt
@module.route('/storages', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def storages():
    if request.method == 'GET':
        storages = Storage.query.all()
        add_form = AddStorageForm()
        return render_template('storage/list.html', storages=storages, add_form=add_form)
    elif request.method == 'POST':
        add_form = AddStorageForm()
        if add_form.validate():
            storage = Storage(add_form.data['name'], add_form.data['path'])
            print storage.name, storage.path
            db.session.add(storage)
            db.session.commit()
            return jsonify(success=True)
        else:
            errors = []
            for field, msg in add_form.errors.iteritems():
                for m in msg:
                    errDict = {
                        'field': field,
                        'error': m,
                    }
                    errors.append(errDict)
            return jsonify(success=False, errors=errors)
    elif request.method == 'PUT':
        pk = request.form.get('pk')
        value = request.form.get('value')
        storage = Storage.query.get(pk)

        if not value:
            return jsonify(success=False, msg='Required')
        if not storage:
            return jsonify(success=False, msg='Storage not found')
        else:
            storage.name = value
            db.session.commit()
            return jsonify(success=True)
    elif request.method == 'DELETE':
        pk = request.form.get('pk')
        value = request.form.get('value')
        storage = Storage.query.get(pk)

        if not current_user.check_password(value):
            return jsonify(success=False, msg='Wrong password')
        if not storage:
            return jsonify(success=False, msg='Storage not found')
        else:
            db.session.delete(storage)
            db.session.commit()
            return jsonify(success=True)