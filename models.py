from sqlalchemy import Column, Integer, String
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

