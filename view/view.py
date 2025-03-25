from flask import Flask,render_template,url_for,Blueprint,request,session,flash,redirect,jsonify
from sqlalchemy.orm import sessionmaker

from db.modle import Users,APICommand,APILink,Fishing,Hooking
from db.mange_db import config,_create_engine
from utility.email_temp import email_temp
from utility.processer import log,getlist

emailTemplate = email_temp()

Session = sessionmaker(bind=_create_engine())
_session = Session()

view = Blueprint("view",__name__,template_folder = "templates")

@view.route("/profile")
# home page with login and singin buttons and some additional info
def profile():
    if "email" in session:
        if request.method != 'GET':
            return redirect(url_for('event.page_404'))
        return render_template('profile.html')
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))

@view.route("/api_command",methods=['GET','POST'])
def api_command():
    if "email" in session:
        try:
            if request.method == 'GET':
                return render_template('api_command.html')
            elif request.method == 'POST':
                CMD = request.json.get('input')
                add_cmd = APICommand(config.ID(n=7),session['email'],CMD,config.CMD_CONDION[0])
                _session.add(add_cmd)
                _session.commit()
                return {'message':'command saved successfully'},200
        except Exception as e:
            print(e)
            _session.rollback()
            log(f"[Error] ocuer at /api_command method={request.method} ,error={e}")
            return redirect(url_for('event.error-500'))
        finally:
            _session.close()

    else:
        flash("you must login first")
        return redirect(url_for("public.login"))

@view.route('/api_command/api')
def api_command_():
    if "email" in session:
        try:
            apiCommand = getlist(_session.query(APICommand).filter_by(email=session['email']).all(),sp=',')
            return jsonify({'allCommand': apiCommand}),200
            ...
        except Exception as e:
            log(f"[Error] ocuer at /_api_command method={request.method} ,error={e}")
            _session.rollback()
            return {'error': 'Server side Error'},500
        finally:
            _session.close()
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))


@view.route("/api_link")
def api_link():
    if "email" in session:
        return render_template('api_link.html')
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))


@view.route("/fishing")
def fishing():
    if "email" in session:
        return render_template('api_link.html')
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))


@view.route("/hooking")
def hooking():
    if "email" in session:
        return render_template('api_link.html')
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))


@view.route("/code")
def code():
    if "email" in session:
        return render_template('api_link.html')
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))
