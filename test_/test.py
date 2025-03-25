from sqlalchemy.orm import sessionmaker
import subprocess

from db.modle import APICommand
from db.mange_db import config,_create_engine
from utility.processer import log,getlist,read_from_json,writeToJson


Session = sessionmaker(bind=_create_engine())
_session = Session()
data = read_from_json()

commands = getlist(_session.query(APICommand).all(),sp=',')
def json_me():
    for command in commands:
        cmd = subprocess.Popen(command[2],shell=True,stderr=subprocess.PIPE,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        output_bytes = cmd.stderr.read() + cmd.stdout.read()
        string = str(output_bytes,'utf-8')
        cmd_data = {command[0] : string}
        print(cmd_data)
        writeToJson(data=data,section='output',info=cmd_data)

