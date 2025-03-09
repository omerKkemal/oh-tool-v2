from flask import Blueprint,jsonify,request,session

api = Blueprint('api',__name__)

@api.route('/api/ApiCommand',methods=['POST','GET'])
def apiCommand():
    if 'email' in session:
        if request.method == 'POST':
            ...
        elif request.method == 'GET':
            ...
        else:
            ...
