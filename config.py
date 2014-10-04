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
	SQLALCHEMY_DATABASE_URI = str(os.environ.get('DATABASE_URL', 'postgres://lihzvhzpvtdlab:wg0oQhLscl-gaxtvmAMzP9S7VM@ec2-54-225-243-113.compute-1.amazonaws.com:5432/d3u7hnmcll7rof'))
	#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'appnew.db')

config = {
	'default': ProductionConfig
}