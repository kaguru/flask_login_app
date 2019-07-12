from sqlalchemy import Column, String, Integer
from .db import Base
from flask_login import UserMixin


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class UserActive(UserMixin):
    def __init__(self, id):
        self.id = id


def create_tables(engine):
    Base.metadata.create_all(bind=engine)
