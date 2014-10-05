Twitter Bot
-----------

This project is also a skeleton of a "Large" Flask application with Twitter bootstrap integration.

### Twitter bot

This is the remote url for the app

~~~sh
$ git remote set-url origin https://github.com/rahulrrixe/twitterbot.git

or

$ git remote set-url origin git@github.com:rahulrrixe/twitterbot.git
~~~

![Index pic](http://i.imgur.com/f2xI37r.png?1 "index")
** index.html **

Requirements
---
* Python 2.7 or 2.6
* Sqlite
* pip

Getting started
---

Clone the repo to your computer in the desired folder:

~~~ sh
$ git clone https://github.com/rahulrrixe/twitterbot.git
~~~

Use the requirements.txt to start dependencies in your virtualenv:

~~~ sh
$ pip install -r requirements.txt
~~~

Start the server:

~~~ sh
$ fab run
or
$ fab grun # for gunicorn server
~~~

Open the browser; `http://localhost:5000` or with the terminal(OS X):

~~~ sh
$ open http://localhost:5000
~~~

Initialize db
---

Set the db parameters in the default_settings.py or in the production.cfg file and start python interactive shell within the flask environment:

~~~ sh
$ python runserver.py db init
$ python runserver.py db migrate
$ python runserver.py db upgrade
~~~
or
~~~ sh
$ fab shell
>>> db.create_all()
>>> exit()
~~~

***note: You must first create the database in Postgresql. From running this command on heroku, you will need to use heroku run "fab shell"***

Unit testing
---

Add unittests to the manage_tests.py file and then start running the tests:

~~~ sh
$ fab tests
~~~

Production Configuration
---
The cofiguration is given in config.py

***For Heroku using gunicorn and production settings, do the following:***.

**Heroku Postgresql Database** as primary,
Check [heroku](https://devcenter.heroku.com/articles/heroku-postgresql#establish-primary-db).


Alembic Migrations
---

The flask-bootstrap skeleton now supports migrations using Alembic and Flask-SQLAlchemy. [Auto Generating Migrations](http://alembic.readthedocs.org/en/latest/tutorial.html#auto-generating-migrations) are working!

~~~ sh
$ python runserver.py db -m "Added users table"
~~~

Contribute
---
1. Fork the repository on Github.
2. Send a pull request and don't forget to add yourself to the AUTHORS.md file.

