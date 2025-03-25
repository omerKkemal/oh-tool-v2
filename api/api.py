from flask import Blueprint,jsonify,request,session
from sqlalchemy.orm import sessionmaker

from db.modle import APICommand,APILink
from db.mange_db import config,_create_engine
from utility.email_temp import email_temp
from utility.processer import log,getlist

emailTemplate = email_temp()

Session = sessionmaker(bind=_create_engine())
_session = Session()

api = Blueprint('api',__name__)

@api.route('/api/ApiCommand',methods=['POST','GET'])
def apiCommand():
    if 'email' in session:
        if request.method == 'POST':
            try:
                apiCommand = getlist(_session.query(APICommand).filter_by(email=session['email']).all(),sp=',')
                return {'allCommand': apiCommand},200
                ...
            except Exception as e:
                log(f"[Error] ocuer at /_api_command method={request.method} ,error={e}")
                _session.rollback()
                return {'error': 'Server side Error'},500
            finally:
                _session.close()
        elif request.method == 'GET':
            ...
        else:
            ...
