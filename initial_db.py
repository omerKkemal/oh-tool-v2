'# File: initial_db.py'
# -*- coding: utf-8 -*-
"""
SpecterPanel - Initial Database Setup
This script initializes the database by creating all necessary tables.
It uses SQLAlchemy to manage the database schema.
"""
from db.mange_db import _create_engine, create_all_db_tables

# Create all tables in the database
print(create_all_db_tables(_create_engine()))