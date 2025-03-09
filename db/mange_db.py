import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.modle import Users, APICommand, APILink, Fishing, Hooking, Base
from utility.setting import Setting

# Initialize settings and set variables
config = Setting()
config.setting_var()
def _create_engine():
    return create_engine(config.DB_URI)


def create_all_db_tables(_engine):
    Base.metadata.create_all(_engine)
    return 'database was created successfully along with the table'
