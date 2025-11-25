from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from sqlalchemy.orm import sessionmaker

from db.mange_db import _create_engine, config
import traceback
from utility.processer import log, getlist, readFromJson, delete_data

Session = sessionmaker(bind=_create_engine())
_session = Session()

code_injection_panel = Blueprint('code_injection_panel', __name__, template_folder='templates', static_folder='static', static_url_path='/static')

# view all code injections for the logged-in user
@code_injection_panel.route("/code", methods=["GET", "POST"])
def code():
    """
    Render the code page for the logged-in user.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
        try:
            return render_template('auth/code.html')
        except Exception as e:
            print(e)
            _session.rollback()
            log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
            return redirect(url_for('event.page_500'))
        finally:
            _session.close()
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))