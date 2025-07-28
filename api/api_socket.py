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

api_socket = Blueprint('api_socket', __name__)

@api_socket.route("/api/socket/<target_name>", methods=['GET', 'POST'])
def socket(target_name=None):
    """API endpoint to manage socket connections for targets.
    This endpoint allows clients to connect or disconnect from a target's socket
    and retrieve the current socket status.
    Args:
        target_name (str): The name of the target for which socket management is being requested.
    Returns:
        JSON response indicating the status of the socket connection.
        If the request is a POST request, it updates the socket status based on the provided token.
        If the request is a GET request, it retrieves the current socket status for the target.
    """
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