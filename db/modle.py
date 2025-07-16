# -*- coding: utf-8 -*-
"""
SpecterPanel - Database Models
This module defines the database models for the SpecterPanel application.
These models represent the structure of the database tables
and are used to interact with the database using SQLAlchemy.
It includes models for users, API tokens, targets,
instructions, API commands, API links, and botnets.
Each model is defined as a class that inherits from SQLAlchemy's Base class.
The models include attributes that correspond to the columns in the database tables,
and they provide methods for initialization and representation.
"""

from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = 'USERS'
    email = Column(String(50), primary_key=True)
    password = Column(String(20))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return f"[{self.email},{self.password}]"


class ApiToken(Base):
    __tablename__ = 'API_TOKEN'
    ID = Column(String, primary_key=True)
    token = Column(String(50))
    user_email = Column(String(20),ForeignKey('USERS.email'))

    def __init__(self, ID, token, user_email):
        self.ID = ID
        self.token = token
        self.user_email = user_email

    def __repr__(self):
        return f"[{self.ID},{self.token},{self.user_email}]"


class Targets(Base):
    __tablename__ = 'TARGETS'
    target_name = Column(String(50),primary_key=True)
    user_email = Column(String(20),ForeignKey('USERS.email'))
    token = Column(String,ForeignKey('API_TOKEN.token'))

    def __init__(self, target_name, user_email,token):
        self.target_name = target_name
        self.user_email = user_email
        self.token = token

    def __repr__(self):
        return f"[{self.target_name},{self.user_email},{self.token}]"

# only hold one information per a person and it will get update everytime he/she change Instraction
class Instraction(Base):
    __tablename__ = 'INSTRACTION'
    ID = Column(String, primary_key=True)
    delay = Column(Integer)
    target_name = Column(String,ForeignKey('TARGETS.target_name'),primary_key=True)
    instraction = Column(String)
    stutas = Column(String)

    def __init__(self ,ID , delay, target_name, instraction,stutas):
        self.ID = ID
        self.delay = delay
        self.target_name = target_name
        self.instraction = instraction
        self.stutas = stutas # active and Inactive


    def __repr__(self):
        return f"[{self.ID},{self.delay},{self.target_name},{self.instraction},{self.stutas}]"


class APICommand(Base):
    __tablename__ = 'API_COMMAND'
    ID = Column(String, primary_key=True)
    email = Column(String(20), ForeignKey('USERS.email'))
    target_name = Column(String,ForeignKey('TARGETS.target_name'))
    cmd = Column(String(20))
    condition = Column(Text)
    update = Column(String)  # update for no notYet, 1 for update

    def __init__(self, ID, email, target_name, cmd, condition, update='unchecked'):
        self.ID = ID
        self.email = email
        self.target_name = target_name
        self.cmd = cmd
        self.condition = condition
        self.update = update

    def __repr__(self):
        return f"[{self.ID},{self.email},{self.target_name},{self.cmd},{self.condition},{self.update}]"


class APILink(Base):
    __tablename__ = 'API_LINK'
    ID = Column(String, primary_key=True)
    email = Column(String(20), ForeignKey('USERS.email'))
    target_name = Column(String,ForeignKey('TARGETS.target_name'))
    link = Column(String(20))
    action_type = Column(Text)
    condition = Column(Integer)

    def __init__(self, ID, email, target_name, link, action_type, condition):
        self.ID = ID
        self.email = email
        self.target_name = target_name
        self.link = link
        self.action_type = action_type
        self.condition = condition

    def __repr__(self):
        return f"[{self.ID},{self.email},{self.target_name},{self.link},{self.action_type},{self.condition}]"


class BotNet(Base):
    __tablename__ = 'BOT_NET'
    ID = Column(String, primary_key=True)
    token = Column(String,ForeignKey('API_TOKEN.token'))
    target_name = Column(String,ForeignKey('TARGETS.target_name'))
    botNetType = Column(String)
    status = Column(String)

    def __init__(self , ID, target_name, botNetType, token, status):
        self.ID = ID
        self.token = token
        self.target_name = target_name
        self.botNetType = botNetType
        self.status = status


    def __repr__(self):
        return f"[{self.ID},{self.token},{self.target_name},{self.botNetType},{self.status}]"
