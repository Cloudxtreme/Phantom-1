#-*- coding: utf-8 -*-
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, AnonymousUserMixin, login_user, logout_user, login_required, current_user
from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand

from functools import wraps

app = Flask(__name__)
app.config.from_object('config')

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'phantom.login'
login_manager.login_message = u'로그인이 필요한 페이지입니다.'
login_manager.anonymous_user = AnonymousUserMixin
login_manager.init_app(app)

manager = Manager(app)
server = Server(host="0.0.0.0", port=5000, threaded=True)
manager.add_command('runserver', server)
manager.add_command('db', MigrateCommand)

# for migrations
from phantom.models import *

# for flask-login
@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

def logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated():
            return 'anonymous required'
        else:
            return func(*args, **kwargs)
    return decorated_function

@app.errorhandler(404)
def not_found(error):
    return '404', 404

from phantom.views import module as app_module
app.register_blueprint(app_module)
