import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
RELOAD = False
CSRF_ENABLED = True
SECRET_KEY = 'notmysecretkey'
#SQLALCHEMY_DATABASE_URI = str(os.environ.get('DATABASE_URL', 'postgresql://localhost/myproddatabase'))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db)