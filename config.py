import os

basedir = os.path.abspath(os.path.dirname(__file__))

# config file for production
class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'thisI$immp0sibble334!22@'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	FLASKY_MAIL_SUBJECT_PREFIX = 'WHO KNOWS'
	FLASKY_MAIL_SENDER = 'ME <ME@EXAMPLE.COM>'
	FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'admin'
	DEBUG = False
	RELOAD = False
	CSRF_ENABLED = True

	@staticmethod
	def init_app(app):
		pass

class ProductionConfig(Config):
	if os.environ.get('DATABASE_URL'):
		SQLALCHEMY_DATABASE_URI = str(os.environ.get('DATABASE_URL'))
	else:
		SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'appnew.db')

	BROKER_URL=os.environ.get('REDISTOGO_URL', 'redis://localhost')
	CELERY_RESULT_BACKEND=os.environ.get('REDISTOGO_URL', 'redis://localhost')
	CELERY_TASK_SERIALIZER='json'
	CELERY_ACCEPT_CONTENT=['json', 'msgpack', 'yaml']

config = {
	'default': ProductionConfig
}