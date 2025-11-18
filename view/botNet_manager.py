from flask import Blueprint, request, render_template, redirect, url_for, session, flash, jsonify
from sqlalchemy.orm import sessionmaker

from db.mange_db import _create_engine, config
import traceback
from db.modle import BotNet, Targets, APILink
from utility.processer import log, getlist

Session = sessionmaker(bind=_create_engine())
_session = Session()

botNet_manager = Blueprint('botNet_manager', __name__, template_folder='templates', static_folder='static', static_url_path='/static')

# view all botNets for the logged-in user
@botNet_manager.route("/api_link", methods=["GET", "POST"])
def api_link():
    """
    Manage API links for the logged-in user.
    GET: Display existing API links and targets.
    POST: Add a new API link.
    """
    if "email" not in session:
        flash("You must login first")
        return redirect(url_for("public.login"))

    if request.method == "POST":
        try:
            form = request.form
            print(form)

            # Safely extract values (use None if missing)
            target_name = form.get("target_name")
            link = form.get("link")
            action_type = form.get("type")
            condition = form.get("condition", config.CONDEITION[0])
            port = form.get("port")
            threads = form.get("threads")
            username = form.get("username")
            password = form.get("password")

            # Convert numeric values properly
            port = int(port) if port and port.isdigit() else None
            threads = int(threads) if threads and threads.isdigit() else None

            # Create a single APILink object with safe defaults
            new_link = APILink(
                ID=config.ID(),
                email=session["email"],
                target_name=target_name,
                link=link,
                action_type=action_type,
                condition=condition,
                port=port,
                thread=threads,
                user_name=username,
                password=password,
            )

            _session.add(new_link)
            _session.commit()
            return redirect(url_for("botNet_manager.api_link"))

        except Exception as e:
            _session.rollback()
            log(f"[ERROR ROUTE] {request.endpoint} error: {e}\n{traceback.format_exc()}")
            print("Error:", e)
            return redirect(url_for("event.page_500"))

        finally:
            _session.close()

    # Handle GET requests
    links = _session.query(APILink).filter_by(email=session["email"]).all()
    report = getlist(links, sp=",")
    targetInfo = getlist(_session.query(Targets).filter_by(user_email=session["email"]).all(), sp=",")
    targets = [t[1] for t in targetInfo]

    return render_template("api_link.html", links=links, targets=targets, reports=report)


@botNet_manager.route("/api_link_delete/<ID>")
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
                log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
                return {"message": "Something went wrong"},500
            finally:
                _session.close()
        else:
            flash('unknown link')
            return redirect(request.referrer)
    else:
        flash("You must login first")
        return redirect(url_for("public.login"))


@botNet_manager.route('/api_link_update/<ID>',methods=['POST'])
def link_update(ID):
    """
    Update an existing API link by its ID.
    Only accessible to authenticated users via POST.
    """
    if 'email' in session:
        if request.method == 'POST':
            try:
                update_me = {}
                if 'link' in request.form:
                    update_me['link'] = request.form['link']
                if 'target_name' in request.form:
                    update_me['target_name'] = request.form['target_name']
                if 'action_type' in request.form:
                    update_me['action_type'] = request.form['action_type']
                if 'port' in request.form:
                    update_me['port'] = int(request.form['port'])
                if 'thread' in request.form:
                    update_me['thread'] = request.form['thread']
                _session.query(APILink).filter_by(ID=ID).update(update_me)
                _session.commit()
                return redirect(request.referrer)
            except Exception as e:
                print(e)
                _session.rollback()
                log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
                return redirect(url_for('event.page_500'))
        else:
            return redirect(request.referrer)
    else:
        return redirect(url_for('public.login'))