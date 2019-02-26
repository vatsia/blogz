#from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
#from sqlalchemy.sql import func
from db import db_session
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


class User(db_session.Model, UserMixin):
    __tablename__ = 'users'
    id = db_session.Column(db_session.Integer, primary_key=True)
    name = db_session.Column(db_session.String(64), unique=True)
    password_hash = db_session.Column(db_session.String(256))

    def __init__(self, name=None, password=None):
        self.name = name
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.name

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id).encode('utf-8').decode('utf-8')


class Post(db_session.Model):
    __tablename__ = 'posts'
    id = db_session.Column(db_session.Integer, primary_key=True)
    link_address = db_session.Column(db_session.String, unique=True)
    header = db_session.Column(db_session.String)
    lead_paragraph = db_session.Column(db_session.String)
    content = db_session.Column(db_session.String)
    writer = db_session.Column(db_session.Integer, db_session.ForeignKey('users.id'))
    created = db_session.Column(db_session.DateTime(timezone=True), server_default=db_session.func.now())
    is_draft = db_session.Column(db_session.Boolean)

    def __init__(self, link_address=None, header=None, lead_paragraph=None, content=None, writer=None, is_draft=True):
        self.link_address = link_address
        self.header = header
        self.lead_paragraph = lead_paragraph
        self.content = content
        self.writer = writer
        self.is_draft = is_draft

    def __repr__(self):
        return '<Post %r>' % self.header

