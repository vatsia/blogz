from wtforms import validators, StringField, PasswordField, SubmitField, BooleanField
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    username = StringField(u'Username', [validators.required(), validators.length(max=64)])
    passw = PasswordField(u'Password', [validators.required()])
    remember = BooleanField(u'Remember me')
    button = SubmitField(u'Log in')


class SigninForm(FlaskForm):
    username = StringField(u'username', [validators.required(), validators.length(max=64)])
    passw = PasswordField(u'Password', [validators.required(), validators.length(min=8)])
    passw_confirmation = PasswordField(u'Password confirmation', [validators.required(), validators.length(min=8)])
    button = SubmitField(u'Sign in')

class UpdateUserForm(FlaskForm):
    username = StringField(u'username', [validators.required(), validators.length(max=64)])
    passw = PasswordField(u'Password', [])
    passw_confirmation = PasswordField(u'Password confirmation', [])
    button = SubmitField(u'Update user information')
