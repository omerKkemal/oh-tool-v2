"""
This module manages the database interactions for the application.
It defines functions to create and drop database tables using SQLAlchemy's ORM.
It uses a configuration class to set up the database URI and other settings.
The module includes:
- A function to create a SQLAlchemy engine based on the configuration.
- A function to create all database tables defined in the ORM models.
- A function to drop all database tables defined in the ORM models.
It is designed to be used as part of a Flask application that interacts with a database.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.modle import Users, APICommand, APILink, Base
from utility.setting import Setting

# Initialize settings and set variables
config = Setting()
config.setting_var()
def _create_engine():
    return create_engine(config.DB_URI)


def create_all_db_tables(_engine):
    Base.metadata.create_all(_engine)
    return 'database was created successfully along with the table'

def drop_all_db_tables(_engine):
    Base.metadata.drop_all(_engine)
    return 'database tables were dropped successfully'
