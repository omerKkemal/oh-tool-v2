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
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.modle import SESSION_LOGIN, ApiToken, Users, APICommand, APILink, Base, SESSION_EXPIRE
from utility.processer import update_socket_info
from utility.setting import Setting

# Initialize settings and set variables
config = Setting()
config.setting_var()
def _create_engine():
    return create_engine(config.DB_URI)

SessionLocal = sessionmaker(
    bind=_create_engine(),
    autocommit=False,
    autoflush=False
)

def admin_acount():
    """
    Create an admin account in the database if it does not already exist.
    
    This function checks if an admin user with the email specified in the configuration exists.
    If not, it creates a new admin user with the provided email and password.
    The password is hashed using bcrypt for security.
    
    Returns:
        bool: True if the admin account was created or already exists, False otherwise.
    """
    _session = SessionLocal()
    admin_email = config.ADMIN_EMAIL
    admin_password = config.ADMIN_PASSWORD

    # Check if the admin user already exists
    existing_admin = _session.query(Users).filter_by(email=admin_email).first()
    if existing_admin:
        return True  # Admin account already exists

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Create a new admin user
    new_admin = Users(email=admin_email, password=hashed_password)
    token = config.ID(200)
    apitokn = ApiToken(config.ID(),token,admin_email)
    update_socket_info(token,'offline')
    _session.add(apitokn)
    _session.add(new_admin)
    _session.commit()
    _session.close()
    return True  # Admin account created successfully

def create_all_db_tables(_engine):
    Base.metadata.create_all(_engine)
    return 'database was created successfully along with the table'

def drop_all_db_tables(_engine):
    Base.metadata.drop_all(_engine)
    return 'database tables were dropped successfully'

def SESSION(user_email, flage, session_id=None):
    """
    Manage user sessions in the database.
    
    This function handles three main operations: creating new sessions, deleting existing sessions,
    and checking if a session exists for a user. It interacts with the SESSION_LOGIN database model
    to persist session information.
    
    Args:
        user_email (str): The email address of the user for which to manage the session.
        flage (str): The operation to perform on the session. Valid values are:
            - 'create': Create a new session entry for the user.
            - 'delete': Delete an existing session entry for the user.
            - 'check': Check if a session exists for the user.
        session_id (str, optional): The session ID to use. Defaults to None.
            - For 'create': If not provided, a new random ID is generated using config.ID(20).
            - For 'delete' and 'check': Must be provided to match against the database.
    
    Returns:
        bool: The result of the operation:
            - For 'create': True if the session was successfully created, False otherwise.
            - For 'delete': True if the session was successfully deleted, False otherwise.
            - For 'check': True if a session exists for the user, False otherwise.
            - For invalid flage values: False.
    
    Raises:
        No exceptions are explicitly raised. Database errors are handled internally by SQLAlchemy.
    
    Examples:
        >>> # Create a new session for a user
        >>> SESSION('user@example.com', 'create', 'session_123')
        True
        
        >>> # Check if a session exists
        >>> SESSION('user@example.com', 'check', 'session_123')
        True
        
        >>> # Delete a session
        >>> SESSION('user@example.com', 'delete', 'session_123')
        True
    
    Notes:
        - The function uses SQLAlchemy ORM for database operations.
        - Each operation creates a new SessionLocal instance for database interaction.
        - The 'delete' operation uses filter_by to find and remove matching sessions.
        - The 'create' operation generates a random ID if session_id is not provided.
        - The 'check' operation returns the first matching record or False if none found.
    """
    _session = SessionLocal()

    sessions = _session.query(SESSION_LOGIN).filter_by(email=user_email).all()
    for session in sessions:
        exp_session = _session.query(SESSION_EXPIRE).filter_by(session_id=session.session_id)
        for exp in exp_session:
            created_at = exp.created_at
            how_long = exp.how_long
            if config.is_session_expired(created_at, how_long):
                _session.query(SESSION_LOGIN).filter_by(
                    email=user_email,
                    session_id=session.session_id
                ).delete()
                _session.query(SESSION_EXPIRE).filter_by(
                    session_id=session.session_id
                ).delete()
                _session.commit()
            
    if flage == 'delete':
        if session_id is None:
            return False
        _session.query(SESSION_LOGIN).filter_by(
            email=user_email,
            session_id=session_id
        ).delete()
        _session.query(SESSION_EXPIRE).filter_by(
            session_id=session_id
        ).delete()
        _session.commit()
        return True
    elif flage == 'create':
        new_session = SESSION_LOGIN(
            ID=config.ID(10), 
            email=user_email, 
            session_id=session_id or config.ID(20)
        )
        new_session_expire = SESSION_EXPIRE(
            ID=config.ID(10),
            session_id=new_session.session_id,
            how_long=config.DEFALUT_HOW_LONG,
            created_at=config.get_current_utc_time()
        )
        _session.add(new_session_expire)
        _session.add(new_session)
        _session.commit()
        _session.close()
        return True
    elif flage == 'check':
        if session_id is None:
            return False
        is_login = _session.query(SESSION_LOGIN).filter_by(
            email=user_email,
            session_id=session_id
        ).first()
        if is_login:
            return True
        else:
            return False
    else:
        return False
