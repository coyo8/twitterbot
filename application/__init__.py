from flask import Flask, render_template, session
from flask.ext.sqlalchemy import SQLAlchemy
from celery import Celery
from flask.ext.login import LoginManager
# Create the app and configuration
# Read the configuration file
app = Flask(__name__)
app.config.from_object('application.default_settings')
app.config.from_envvar('PRODUCTION_SETTINGS', silent=True)
app.config['WTF_CSRF_ENABLED'] = False

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

def create_celery_app(app):
	celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
	celery.conf.update(app.config)
	Taskbase = celery.Task

	class ContextTask(Taskbase):
		abstract = True

		def __call__(self, *args, **kwargs):
			with app.app_context():
				return Taskbase.__call__(self, *args, **kwargs)
	
	celery.Task = ContextTask
	return celery


celery = create_celery_app(app)
# Connect to database with sqlalchemy.
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)


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

