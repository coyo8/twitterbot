from wtforms import Form, TextField, BooleanField, PasswordField, TextAreaField, validators, SubmitField
from application.models import User
from flask.ext.login import login_user

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])


class TokenForm(Form):
    twitter_handle = TextField('TWITTER HANDLE', validators=[validators.Required()])
    auth_token = TextField('OAUTH TOKEN', validators=[validators.Required()])
    auth_secret = TextField('OAUTH SECRET', validators=[validators.Required()])
    consumer_key = TextField('CONSUMER KEY', validators=[validators.Required()])
    consumer_secret = TextField('CONSUMER SECRET', validators=[validators.Required()])

class HashTagForm(Form):
    hashtag = TextField('Hash Tags', validators=[validators.Required()])

try:
	from flask.ext.wtf import Form
except ImportError:
	print "Not WTF module"

class LoginForm(Form):
    username = TextField('Username')
    password = PasswordField('Password')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            username=self.username.data).first()

        if user is None:
            self.username.errors.append('Unknown username')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        login_user(user)

        return True


