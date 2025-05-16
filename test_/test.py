from sqlalchemy.orm import sessionmaker
import subprocess

from db.modle import APICommand,Targets
from db.mange_db import config,_create_engine
from utility.processer import getlist# read_from_json,writeToJson


Session = sessionmaker(bind=_create_engine())
_session = Session()
# data = read_from_json()

def json_me():
    commands = getlist(_session.query(APICommand).all(),sp=',')
    for command in commands:
        result = subprocess.run(command[2], shell=True, capture_output=True, text=True)
        output_bytes = result.stderr + result.stdout
        output_string = str(output_bytes,'utf-8')
        cmd_data = {command[0] : output_string}
        print(cmd_data)
        writeToJson(data=data,section='output',info=cmd_data)

def tt():
    targets = getlist(_session.query(Targets).filter_by(user_email=' omerkemal2019@gmail.com').all(),sp=',')
    print(targets)

# 
"""
if request.method == 'POST':
        try:
            ...
        except Exception as e:
            log(f'[ERROR ROUT] : {request.endpoint} error: {e}')
            return {'Erorr': 'Invalid api_token or no api token provided'},404
    else:
        return {'Error': "Unsupported method or didn't provid target name"},405
"""