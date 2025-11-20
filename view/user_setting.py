from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from sqlalchemy.orm import sessionmaker
from db.mange_db import _create_engine, config
from db.modle import Users, ApiToken, Instruction_Detail
import bcrypt
import traceback
from utility.processer import log, getlist

Session = sessionmaker(bind=_create_engine())
_session = Session()

user_setting = Blueprint('user_setting', __name__, template_folder='templates', static_folder='static', static_url_path='/static')

@user_setting.route("/settings",methods=['POST','GET'])
def setting():
    """
    Render the settings page for the logged-in user.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
        try:
            user_email = session['email']
            user_instructions = _session.query(Instruction_Detail).filter_by(userEmail=user_email).all()
            token = getlist(_session.query(ApiToken).filter_by(user_email=session['email']).all(), sp=',')
            return render_template('setting.html',token=token,user_instructions=user_instructions)
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
# settings for user information update
@user_setting.route("/update_user_info", methods=['POST'])
def update_user_info():
    """
    Update user information for the logged-in user.
    Redirects to login if the user is not authenticated.
    """
    if "email" in session:
        if request.method == 'POST':
            try:
                user = _session.query(Users).filter_by(email=session["email"]).first()
                email = request.form['email']
                email_bool = request.form['email'] == session['email']
                old_password = bcrypt.checkpw(request.form['old_password'].encode('utf-8'), user.password.encode('utf-8'))
                print(old_password)
                password = request.form['password']
                confirm_password = request.form['confirm_password']
                if password != confirm_password:
                    flash("Passwords do not match.")
                    return jsonify({"error": "Passwords do not match"}), 400
                # Update user information in the database
                if not old_password:
                    return jsonify({"error": "Incorrect old password"}), 400
                if not user:
                    return jsonify({"error": "User not found"}), 404
                if email_bool:
                    _session.query(Users).filter_by(email=session["email"]).update({
                        'password': bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    })
                    _session.commit()
                    return jsonify({"message": "Email already exists, password updated"}), 200
                _session.query(Users).filter_by(email=session["email"]).update({
                    'email': email,
                    'password': bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                })
                _session.commit()
                return jsonify({"message": "User information updated successfully."}), 200
            except Exception as e:
                print(e)
                _session.rollback()
                log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
                return jsonify({"error": "An error occurred while updating user information."}), 500
            finally:
                _session.close()
        else:
            return jsonify({"error": "Invalid request method"}), 405
    else:
        return jsonify({"error": "User not authenticated"}), 401

# setting generate api token

@user_setting.route('/apiToken/generate', methods=['POST'])
def apiToken_generate():
    '''
    Generate a new API token for the authenticated user.
    This route creates a new API token associated with the logged-in user's email.
    It requires the user to be logged in and uses a POST request to generate the token.
    Returns a JSON response with the generated token or an error message.
    '''
    if 'email' in session:
        if request.method != 'POST':
            return jsonify({"error": "Invalid request method"}), 405
        try:
            new_token = ApiToken(
                ID=config.ID(),
                token=config.ID(n=200),
                user_email=session['email']
            )
            _session.add(new_token)
            _session.commit()
            return jsonify({"message": "API token generated successfully.", "api_token": new_token.token, "id": new_token.ID}), 200
        except Exception as e:
            print(e)
            _session.rollback()
            log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
            return jsonify({"error": "An error occurred while generating API token."}), 500
        finally:
            _session.close()
    else:
        return jsonify({"error": "User not authenticated"}), 401


# delete apiToken
@user_setting.route('/apiToken/delete/<ID>', methods=['DELETE'])
def apiToken_delete(ID=None):
    '''
    Delete an API token by its ID for the authenticated user.
    This route allows the logged-in user to delete an API token they own by specifying its ID
    in the URL. It requires the user to be logged in and uses a DELETE request.
    Returns a JSON response indicating success or failure of the deletion.
    '''
    if 'email' in session:
        try:
            apiToken = _session.query(ApiToken).filter_by(user_email=session['email'], ID=ID).first()
            if apiToken:
                _session.delete(apiToken)
                _session.commit()
                return jsonify({"message": "API token deleted successfully."}), 200
            else:
                return jsonify({"error": "API token not found."}), 404
        except Exception as e:
            print(e)
            _session.rollback()
            log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
            return jsonify({"error": "An error occurred while deleting API token."}), 500
        finally:
            _session.close()
    else:
        return jsonify({"error": "User not authenticated"}), 401

@user_setting.route("/set_user_instruction", methods=['POST'])
def user_instruction():
    if 'email' in session:
        try:
            user_email = session['email']
            user_instructions = _session.query(Instruction_Detail).filter_by(userEmail=user_email).all()
            return jsonify({"user_instructions": [ins.to_dict() for ins in user_instructions]}), 200
        except Exception as e:
            print(e)
            log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
            return jsonify({"error": "An error occurred while retrieving user instructions."}), 500
    else:
        return jsonify({"error": "User not authenticated"}), 401