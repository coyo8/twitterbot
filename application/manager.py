from application import app, lm, db
from flask import session, redirect, url_for, request, flash, render_template, g, session
from flask.ext.login import login_user, logout_user, current_user, login_required
from application.models import *
from application.form import *


@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@app.route('/index')
def index():
    return render_template('info/index.html', title='Flask Twitter Scraper')


@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		user = User(form.username.data, form.email.data,
                    form.password.data)
		db.session.add(user)
		flash('Thanks for registering')
		return redirect(url_for('login'))
	return render_template('info/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
    	print "hi I am here"
        flash(u'Successfully logged in as %s' % form.user.username)
        session['user_id'] = form.user.id
        #return redirect(url_for('index'))
        return "Hi done"
    return render_template('info/login.html', form=form)

@app.route('/home/<username>/')
@login_required
def home(username):
    return render_template('info/hello.html', title="Flask-App, Hi %s"
                            % (username), username=username)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('index')