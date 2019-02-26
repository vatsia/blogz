#from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
#from sqlalchemy.sql import func
from db import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(256))

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


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    link_address = db.Column(db.String, unique=True)
    header = db.Column(db.String)
    lead_paragraph = db.Column(db.String)
    content = db.Column(db.String)
    writer = db.Column(db.Integer, db.ForeignKey('users.id'))
    created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    is_draft = db.Column(db.Boolean)

    def __init__(self, link_address=None, header=None, lead_paragraph=None, content=None, writer=None, is_draft=True):
        self.link_address = link_address
        self.header = header
        self.lead_paragraph = lead_paragraph
        self.content = content
        self.writer = writer
        self.is_draft = is_draft

    def __repr__(self):
        return '<Post %r>' % self.header

