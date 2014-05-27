#-*- coding: utf-8 -*-
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, AnonymousUserMixin, login_user, logout_user, login_required, current_user
from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand
from flask_wtf.csrf import CsrfProtect
from celery import Celery
from functools import wraps

# flask app
app = Flask(__name__)
app.config.from_object('config')
csrf = CsrfProtect(app)

# jinja environment
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# login manager
login_manager = LoginManager()
login_manager.login_view = 'phantom.login'
login_manager.login_message = 'Login required'
login_manager.anonymous_user = AnonymousUserMixin
login_manager.init_app(app)

# manager
manager = Manager(app)
@manager.command
def beat():
    import shlex
    from subprocess import call
    call(shlex.split('celery worker -A app.celery -B'))
server = Server(host="0.0.0.0", port=5000, threaded=True)
manager.add_command('runserver', server)
manager.add_command('db', MigrateCommand)
# manager.add_command('beat', start_celery_beat)

# for migrations
from phantom.models import *

# celery
def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

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
