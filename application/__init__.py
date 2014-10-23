from flask import Flask, render_template, session
from flask.ext.sqlalchemy import SQLAlchemy
from celery import Celery
from flask.ext.login import LoginManager
from config import config
import os
# Create the app and configuration
# Read the configuration file
db = SQLAlchemy()
lm = LoginManager()


app = Flask(__name__)
app.config.from_object(config['default'])
app.config['WTF_CSRF_ENABLED'] = False

# Connect to database with sqlalchemy.
lm.init_app(app)
db.init_app(app)

def create_celery_app(app=None):
	celery = Celery(app.import_name)
	celery.conf.update(app.config)
	Taskbase = celery.Task

	class ContextTask(Taskbase):
		abstract = True

		def __call__(self, *args, **kwargs):
			with app.app_context():
				return Taskbase.__call__(self, *args, **kwargs)

	celery.Task = ContextTask
	# very important line for app context
	celery.app = app
	return celery

celery = create_celery_app(app)

# 404 page not found "route"
@app.errorhandler(404)
def not_found(error):
	title = "404 Page not found"
	return render_template('404.html', title=title), 404


# 500 server error "route"
@app.errorhandler(500)
def server_error(error):
    title = "500 Server Error"
    db.session.rollback()
    return render_template('500.html', title=title), 500

import application.manager

