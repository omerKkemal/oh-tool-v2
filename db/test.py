from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class land(Base):
    __tablename__ = 'LANDS'

    def __init__(self):
        ...
    def __repr__(self):
        ...

class user(Base):
    __tablename__ = 'USER'

    def __init__(self):
        ...
    def __repr__(self):
        ...