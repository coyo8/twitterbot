import os
from application import app, db
from application.models import *
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app.debug = True
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
	return dict(app=app, db=db)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def dropdb():
    if prompt_bool(
        "Are you sure you want to lose all your data"):
        db.drop_all()

@manager.command
def create(default_data=True, sample_data=False):
    "Creates database tables from sqlalchemy models"
    db.create_all()
    populate(default_data, sample_data)

@manager.command
def recreate(default_data=True, sample_data=False):
    "Recreates database tables (same as issuing 'drop' and then 'create')"
    drop()
    create(default_data, sample_data)

# run the application!
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    manager.run()
