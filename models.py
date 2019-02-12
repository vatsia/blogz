from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from db import Base
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    password_hash = Column(String(256))

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


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    link_address = Column(String, unique=True)
    header = Column(String)
    lead_paragraph = Column(String)
    content = Column(String)
    writer = Column(Integer, ForeignKey('users.id'))
    created = Column(DateTime(timezone=True), server_default=func.now())
    is_draft = Column(Boolean)

    def __init__(self, link_address=None, header=None, lead_paragraph=None, content=None, writer=None, is_draft=True):
        self.link_address = link_address
        self.header = header
        self.lead_paragraph = lead_paragraph
        self.content = content
        self.writer = writer
        self.is_draft = is_draft

    def __repr__(self):
        return '<Post %r>' % self.header

