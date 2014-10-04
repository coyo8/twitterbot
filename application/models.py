from application import db

#
#Create your own models here and they will be imported automaticaly. or
#use a model per blueprint.

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    auth_token = db.Column(db.String(80), nullable=False)
    auth_secret = db.Column(db.String(80), nullable=False)
    consumer_key = db.Column(db.String(80), nullable=False)
    consumer_secret = db.Column(db.String(80), nullable=False)
    job_status = db.Column(db.Boolean(), nullable=False)


    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.auth_token = ''
        self.auth_secret = ''
        self.consumer_key = ''
        self.consumer_secret = ''
        self.job_status = False


    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        if self.password == password:
            return True

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Hashtag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(100), unique=True)

    def __init__(self, tag):
        self.tag = tag


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    hostname = db.Column(db.String(20))
    flagger = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='log', lazy='')

    def __init__(self, time, uptime, hostname, flagger, user_id):
        self.returns = 0
        self.errors = 0
        self.time = time
        self.hostname = hostname
        self.flagger = flagger
        self.user_id = user_id

    def __repr__(self):
        return '<Log %r>' % (self.hostname)
