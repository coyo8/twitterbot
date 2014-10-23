from application import app, lm, db
from flask import session, redirect, url_for, request, flash, render_template, g, session
from flask.ext.login import login_user, logout_user, current_user, login_required
from application.models import User, Hashtag
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

    if current_user.is_authenticated():
        flash('Please logout to register as a new user')
        return redirect(url_for("home", user=g.user))

    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('info/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        flash('Already logged in')
        return redirect(url_for("home", user=g.user))

    form = LoginForm()
    if form.validate_on_submit():
        flash(u'Successfully logged in as %s' % form.user.username)
        session['user_id'] = form.user.id
        return redirect(url_for('home', user=g.user))
    return render_template('info/login.html', form=form)

@app.route('/user')
def user():
    if current_user.is_authenticated():
        return redirect(url_for("home", username=current_user.username))
    else:
        return render_template('info/hello.html', title="Hi Guest!" , user=g.user)

@app.route('/home')
@login_required
def home():
    user = User.query.filter_by(id=g.user.id).first()
    return render_template('info/hello.html', title="Hi %s"
                            % (user.username), user=user)

@app.route('/token', methods=['GET', 'POST'])
@login_required
def token():
    form = TokenForm(request.form)
    user = User.query.filter_by(username=current_user.username).first()
    if request.method == 'POST' and form.validate():
        user.twitter_handle = form.twitter_handle.data
        user.auth_token = form.auth_token.data
        user.auth_secret = form.auth_secret.data
        user.consumer_key = form.consumer_key.data
        user.consumer_secret = form.consumer_secret.data
        db.session.commit()
        flash('Successfully added the token')
        return redirect(url_for("index"))
    return render_template('info/token.html', form=form)

@app.route('/hashtag', methods=['GET', 'POST'])
@login_required
def hashtag():
    form = HashTagForm(request.form)
    disp_hashtag = Hashtag.query.filter_by(user_id=g.user.id).all()
    if request.method == 'POST' and form.validate():
        hashtag = Hashtag(form.hashtag.data)
        hashtag.user_id = g.user.id
        print form.hashtag.data
        db.session.add(hashtag)
        flash('HashTag added')
        db.session.commit()
        return redirect(url_for('hashtag'))
    return render_template('info/hashtag.html', form=form, disp_hashtag=disp_hashtag)

@app.route('/hashtag/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_hashtag(id):
    del_tag = Hashtag.query.filter_by(id=id).first()
    if del_tag and del_tag.user_id == g.user.id:
        db.session.delete(del_tag)
        db.session.commit()
        flash('HashTag Deleted succesfully')
    return redirect(url_for('hashtag'))

@app.route('/toggle', methods=['GET', 'POST'])
@login_required
def toggle():
    user = User.query.filter_by(id=g.user.id).first()
    if user:
        if user.job_status == True:
            user.job_status = False
        else:
            user.job_status = True
    db.session.add(user)
    db.session.commit()
    flash('Job status changed')
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect('index')
