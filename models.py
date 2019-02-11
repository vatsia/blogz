#from app.routes import login_manager
from sqlalchemy import Column, Integer, String, Boolean
from db import Base
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    is_authenticated = Column(Boolean)
    is_active = Column(Boolean)
    is_anonymous = Column(Boolean)
    password_hash = Column(String(256))

    def __init__(self, name=None, is_authenticated=None, is_active=None, is_anonymous=None, password=None):
        self.name = name
        self.is_authenticated = is_authenticated
        self.is_active = is_active
        self.is_anonymous = is_anonymous
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.name

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(id).encode('utf-8').decode('utf-8')


#@login_manager.user_loader
#def load_user(user_id):
#    return User.query.get(user_id)
