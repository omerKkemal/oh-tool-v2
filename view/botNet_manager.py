"""
botNet_manager.py
This module defines the routes and views for managing bot networks in the web application.
It handles API link management, including adding, updating, and deleting API links.
It uses Flask for web framework and SQLAlchemy for database interactions.
uses a session to interact with the database.
It also provides functionality to view existing API links and associated targets.
It is part of a Flask application and uses SQLAlchemy for ORM.
It is designed to be used as a Flask Blueprint, allowing it to be registered with the main Flask application.
It includes error handling and logging for debugging purposes.

Routes:
    - '/api_link' : Manage API links for the logged-in user (GET and POST)
    - '/api_link_delete/<ID>' : Delete an API link by its ID (GET)
    - '/api_link_update/<ID>' : Update an existing API link by its ID (POST)
    - 'SESSION(user_email, flage, session_id=None)' : Manage user sessions (create, delete, check)
"""

from flask import Blueprint, request, render_template, redirect, url_for, session, flash, jsonify
from sqlalchemy.orm import sessionmaker

from db.mange_db import _create_engine, config
import traceback
from db.modle import SESSION_LOGIN, BotNet, Targets, APILink
from utility.processer import log, getlist

SessionLocal = sessionmaker(
    bind=_create_engine(),
    autocommit=False,
    autoflush=False
)

botNet_manager = Blueprint('botNet_manager', __name__, template_folder='templates', static_folder='static', static_url_path='/static')



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
    if flage == 'delete':
        _session.query(SESSION_LOGIN).filter_by(
            email=user_email,
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
        _session.add(new_session)
        _session.commit()
        _session.close()
        return True
    elif flage == 'check':
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



# view all botNets for the logged-in user
@botNet_manager.route("/api_link", methods=["GET", "POST"])
def api_link():
    """
    Manage API links for the logged-in user.
    GET: Display existing API links and targets.
    POST: Add a new API link.
    """
    if "email" not in session:
        flash("You must login first")
        return redirect(url_for("public.login"))
    is_login = SESSION(session["email"], "check", session.get("session_id"))
    if not is_login:
        flash("You must login first")
        return redirect(url_for("public.login"))
    _session = SessionLocal()

    if request.method == "POST":
        try:
            form = request.form
            print(form)

            # Safely extract values (use None if missing)
            target_name = form.get("target_name")
            link = form.get("link")
            action_type = form.get("type")
            condition = form.get("condition", config.CONDEITION[0])
            port = form.get("port")
            threads = form.get("threads")
            username = form.get("username")
            password = form.get("password")

            # Convert numeric values properly
            port = int(port) if port and port.isdigit() else None
            threads = int(threads) if threads and threads.isdigit() else None

            # Create a single APILink object with safe defaults
            new_link = APILink(
                ID=config.ID(),
                email=session["email"],
                target_name=target_name,
                link=link,
                action_type=action_type,
                condition=condition,
                port=port,
                thread=threads,
                user_name=username,
                password=password,
            )

            _session.add(new_link)
            _session.commit()
            return redirect(url_for("botNet_manager.api_link"))

        except Exception as e:
            _session.rollback()
            log(f"[ERROR ROUTE] {request.endpoint} error: {e}\n{traceback.format_exc()}")
            print("Error:", e)
            return redirect(url_for("event.page_500"))

        finally:
            _session.close()

    # Handle GET requests
    links = _session.query(APILink).filter_by(email=session["email"]).all()
    report = getlist(links, sp=",")
    targetInfo = getlist(_session.query(Targets).filter_by(user_email=session["email"]).all(), sp=",")
    targets = [t[1] for t in targetInfo]

    return render_template("auth/api_link.html", links=links, targets=targets, reports=report)


@botNet_manager.route("/api_link_delete/<ID>")
def link_delete(ID=None):
    """
    Delete an API link by its ID for the logged-in user.
    Only accessible via GET method.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
        is_login = SESSION(session["email"], "check", session.get("session_id"))
        if not is_login:
            flash("You must login first")
            return redirect(url_for("public.login"))
        _session = SessionLocal()
        if ID:
            if request.method != 'GET':
                flash(f'unknown method {request.method}')
                return redirect(request.referrer)
            try:
                link = getlist(_session.query(APILink).filter_by(ID=ID).all(),sp=',')
                print(link)
                if link:
                    link_ = _session.query(APILink).filter_by(ID=ID).first()
                    _session.delete(link_)
                    _session.commit()
                    flash(f'deleleted sucssesfuly {link[0][3]}')
                    return {"message": "Deleted succsessfully"},200
            except Exception as e:
                print(str(e))
                log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
                return {"message": "Something went wrong"},500
            finally:
                _session.close()
        else:
            flash('unknown link')
            return redirect(request.referrer)
    else:
        flash("You must login first")
        return redirect(url_for("public.login"))


@botNet_manager.route('/api_link_update/<ID>',methods=['POST'])
def link_update(ID):
    """
    Update an existing API link by its ID.
    Only accessible to authenticated users via POST.
    """
    if 'email' in session:
        is_login = SESSION(session['email'], 'check', session.get('session_id'))
        if not is_login:
            flash("You must login first")
            return redirect(url_for('public.login'))
        _session = SessionLocal()
        if request.method == 'POST':
            try:
                update_me = {}
                if 'link' in request.form:
                    update_me['link'] = request.form['link']
                if 'target_name' in request.form:
                    update_me['target_name'] = request.form['target_name']
                if 'action_type' in request.form:
                    update_me['action_type'] = request.form['action_type']
                if 'port' in request.form:
                    update_me['port'] = int(request.form['port'])
                if 'thread' in request.form:
                    update_me['thread'] = request.form['thread']
                _session.query(APILink).filter_by(ID=ID).update(update_me)
                _session.commit()
                return redirect(request.referrer)
            except Exception as e:
                print(e)
                _session.rollback()
                log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
                return redirect(url_for('event.page_500'))
        else:
            return redirect(request.referrer)
    else:
        return redirect(url_for('public.login'))
