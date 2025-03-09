from db.mange_db import _create_engine, create_all_db_tables

# Create all tables in the database
print(create_all_db_tables(_create_engine()))