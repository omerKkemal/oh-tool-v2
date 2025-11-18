from flask import Blueprint, request, render_template, redirect, url_for, session, flash, jsonify
import traceback
import bcrypt
from urllib.parse import unquote
from sqlalchemy.orm import sessionmaker

from db.mange_db import config, _create_engine
from utility.processer import log, getlist, readFromJson, delete_data
from db.modle import APICommand, APILink, Instraction, Targets
from view import view

Session = sessionmaker(bind=_create_engine())
_session = Session()

web_terminal = Blueprint('web_terminal', __name__, template_folder='templates', static_folder='static', static_url_path='/static')

# Web terminal page
@web_terminal.route("/api_command/<targetName>", methods=['GET', 'POST'])
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
                                'status': config.STUTAS[0]
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
                log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
                return redirect(url_for('event.page_500'))
            finally:
                _session.close()
        else:
            flash('please provide target name')
            return redirect(url_for("view.profile")) 

    else:
        flash("you must login first")
        return redirect(url_for("public.login"))


@web_terminal.route('/check_command_update/<target_name>', methods=['GET'])
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
        log(f'[ERROR ROUTE] : {request.endpoint} -> {e}\n{traceback.format_exc()}')
        _session.rollback()
        return jsonify({'error': 'Server side error'}), 500

    finally:
        _session.close()

@web_terminal.route('/api_command/delete',methods=['DELETE'])
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
            log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
            return {'message': 'Something went wrong'}

    else:
        return {'message':"you must login first"}


@web_terminal.route('/api_command/api/<targetName>')
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

            log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
            _session.rollback()
            return {'error': 'Server side Error'}, 500
        
        finally:
            _session.close()
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))
@web_terminal.route("/api_command/botNet/<targetName>")
def api_command_botnet(targetName):
    """
    Return botnet information for the given target and logged-in user.
    Returns JSON response.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
        try:
            botNetInfo = getlist(_session.query(APILink).filter_by(target_name=targetName).all(), sp=',')
            print('-'*10,botNetInfo)
            return jsonify({'botNetInfo': botNetInfo}), 200

        except Exception as e:
            log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
            _session.rollback()
            return jsonify({'error': 'Server side Error'}), 500

        finally:
            _session.close()
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))
