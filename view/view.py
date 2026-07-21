# -*- coding: utf-8 -*-
"""
view.py
This module defines the routes and views for the web application.
It handles user authentication, dashboard rendering, and socket connections for web terminals.
It uses Flask for web framework, SQLAlchemy for database interactions, and Bcrypt for password hashing
and verification.

Routes:
    - '/dashboard' : Dashboard page for logged-in users, displaying targets and connection types.
    - '/socket/<target_name>' : Socket page for a specific target, requires authentication.
"""

import traceback
import bcrypt
from flask import render_template, url_for, Blueprint, request, session, flash, redirect, jsonify
from sqlalchemy.orm import sessionmaker
# from urllib.parse import unquote
# import socket
# import threading

from db.modle import SESSION_LOGIN, Targets, ApiToken, BotNet, APICommand
from db.mange_db import config, _create_engine
# from utility.email_temp import EmailTemplate
from utility.processer import log, getlist, readFromJson, delete_data
# from utility.socket_utility import get_ip, handle_client


SessionLocal = sessionmaker(
    bind=_create_engine(),
    autocommit=False,
    autoflush=False
)

view = Blueprint(
    config.BLUEPRINT_NAME[3],
    __name__, template_folder='templates',
    static_folder='static', static_url_path=config.STATIC_URL_PATH
)
# SOCK_CLINENT = []
# # socket server
# def socket_server_manger(port: int)->None:
#     server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#     host = get_ip()
#     server.bind((host,port))
#     server.listen(5)
#     while True:
#         client, addr = server.accept()
#         log(f'[SOCKET] : new connection from {addr}')
#         SOCK_CLINENT.append(client)
#         threading.Thread(target=handle_client, args=(client,)).start()


def SESSION(user_email, flage, session_id=None):
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
            session_id=config.ID(20)
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
        print(f"[DEBUG] is_login: {is_login}, email: {user_email}, session_id: {session_id}")   
        if is_login:
            return True
        else:
            return False
    else:
        return False


@view.route("/dashboard")
def dashboard():
    """
    Render the dashboard page for the logged-in user.
    Displays targets associated with the user's email.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
        is_login = SESSION(session['email'], 'check', session.get('session_id'))
        print(f"[DEBUG] is_login: {is_login}, email: {session['email']}, session_id: {session.get('session_id')}")
        if not is_login:
            flash("you must login first")
            return redirect(url_for("public.login"))
        _session = SessionLocal()
        try:
            email = session['email']
            print(email)
            pending_command = len(_session.query(APICommand).filter_by(email=session['email'], condition=config.STUTAS[1]).all())
            targets = getlist(_session.query(Targets).filter_by(user_email=session['email']).all(), sp=',')
            botnet_per_targert = {}
            _targets = [] #list of (target_info, conn_type, target_name)
            total_bot = 0
            for target in targets:
                target_ = readFromJson('target-info',target[1])
                print(target_)
                botnet_info = _session.query(BotNet).filter_by(target_name=target[1]).all()
                botnet_per_targert[target[1]] = (len(botnet_info), botnet_info)
                total_bot = total_bot + len(botnet_info)
                if '127.0.0.1' in target_['ip']:
                    conn = 'local'
                elif '192.168' in target_['ip']:
                    conn = 'wifi'
                else:
                    # , mdi mdi-ethernet-cable
                    conn = 'ethernet'
                _targets.append((target_, conn, target[1]))
            botnet_per_targert['totalBot'] = total_bot
            if request.method != 'GET':
                return redirect(url_for('event.page_404'))
            return render_template('auth/dashboard.html', targets=_targets,botnet_per_targert=botnet_per_targert,pending_commands=pending_command)
        except Exception as e:
            log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
            print(traceback.format_exc())
            _session.rollback()
            return redirect(url_for('event.page_500'))
        finally:
            _session.close()
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))



@view.route("/socket/<target_name>")
def socket_page(target_name):
    """
    Render the socket page for a specific target.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
        is_login = SESSION(session['email'], 'check', session.get('session_id'))
        if not is_login:
            flash("you must login first")
            return redirect(url_for("public.login"))
        _session = SessionLocal()
        try:
            token = getlist(_session.query(ApiToken).filter_by(user_email=session['email']).all(), sp=',')[0][1]
            targets = getlist(_session.query(Targets).filter_by(target_name=target_name).all(), sp=',')
            if len(targets) != 0 and len(token) != 0:
                return render_template('auth/socket.html', target_name=target_name,token=token)
            else:
                flash(f'No such a target {target_name}')
                return redirect(request.referrer)
        except Exception as e:
            log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
            _session.rollback()
            return redirect(url_for('event.page_500'))
        finally:
            _session.close()
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))

