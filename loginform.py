from wtforms import Form, validators, StringField, PasswordField, SubmitField, BooleanField

class LoginForm(Form):
    username = StringField(u'Username', [validators.required(), validators.length(max=64)])
    password = PasswordField(u'Password', [validators.required()])
    remember = BooleanField(u'Remember me')
    button = SubmitField(u'Log in')
