"""
Code Injection Panel Blueprint
This module defines the Flask Blueprint for the code injection panel,
which allows users to manage code payloads, inject them into target systems,
and monitor their execution status and outputs.
route: /code_injection_panel ............... it contains:
- View and edit code payloads .............. /code
- Inject code into target systems ........... /code_injection
- Check for updates from injected code ...... /code_injection/check_update
- Retrieve outputs from injected code ..... /code_injection/get_output/<ID>

Note: This module requires user authentication for access and performs database
      operations using SQLAlchemy.
"""

import os
from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from sqlalchemy.orm import sessionmaker

from db.modle import Targets, Instraction, code_injection_payloads
from db.mange_db import _create_engine, config
import traceback
from utility.processer import log, getlist, readFromJson, delete_data

# Create session factory ONLY - no global session
SessionLocal = sessionmaker(bind=_create_engine(), autocommit=False, autoflush=False)

code_injection_panel = Blueprint('code_injection_panel', __name__, 
                                template_folder='templates', 
                                static_folder='static', 
                                static_url_path='/static')


# view all code injections for the logged-in user
@code_injection_panel.route("/code", methods=["GET", "POST"])
def code():
    """
    Render the code page for the logged-in user.
    Redirects to login if the user is not authenticated.
    """
    if "email" not in session:
        flash("You must login first")
        return redirect(url_for("public.login"))
    
    db = SessionLocal()
    try:
        if request.method == "GET":
            # Query inactive code injections
            inactive_code_injections = db.query(code_injection_payloads).filter_by(
                user_status=config.CHECK_UPDATE[1],  # 'unchecked'
                target_staus=config.STUTAS[1]  # 'Inactive'
            ).all()
            
            # Get target names from Instraction table
            target_names = [
                t.target_name for t in db.query(Instraction).filter_by(
                    status=config.STUTAS[1],  # 'Inactive'
                    instraction=config.INSTRACTION[3]  # 'codeInjection'
                ).all()
            ]
            
            # Filter code injections by target names
            inactive_code_injections_filtered = [
                ci for ci in inactive_code_injections 
                if ci.target_name in target_names
            ]
            
            # Extract just the target names
            inactive_code_injections_ids = []
            if inactive_code_injections_filtered:
                # Get unique target names
                inactive_code_injections_ids = list(set([
                    ci.target_name for ci in inactive_code_injections_filtered
                ]))
            
            payloads = os.listdir(config.STATIC_DIR)
            print("Payloads:", payloads)
            
            # Get all targets as list of [id, target_name]
            targets_query = db.query(Targets).all()
            targets = [[target.ID, target.target_name] for target in targets_query]
            
            return render_template(
                'auth/code.html',
                payloads=payloads, 
                targets=targets,
                inactive_code_injections_ids=inactive_code_injections_ids
            )
        else:  # POST method
            flash("No inactive code injections found.")
            return render_template('auth/code.html', 
                                 payloads=[], 
                                 targets=[], 
                                 inactive_code_injections_ids=[])
            
    except Exception as e:
        log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
        return redirect(url_for('event.page_500'))
    finally:
        db.close()

@code_injection_panel.route("/code_injection/load_code/<payload_name>", methods=["GET"])
def load_code(payload_name):
    """
    Load and return the content of a specified code payload.
    args:
        payload_name (str): The name of the payload file to load.
    Returns:
        JSON response containing the content of the payload or an error message.
    """
    if "email" not in session:
        return jsonify({'error': 'Unauthorized access.'}), 401
    
    try:
        file_path = os.path.join(config.STATIC_DIR, payload_name)
        with open(file_path, 'r') as file:
            content = file.read()
        return jsonify({'content': content})
    except Exception as e:
        log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
        return jsonify({'error': 'Failed to load code payload.'}), 500


@code_injection_panel.route("/code_injection/save_code/<payload_name>", methods=["POST"])
def save_code(payload_name):
    """
    Save the content of a code payload to a file.
    args:
        payload_name (str): The name of the payload file to save.
    Returns:
        JSON response indicating success or failure of the save operation.
    """
    if "email" not in session:
        return jsonify({'error': 'Unauthorized access.'}), 401
    
    try:
        content = request.json.get('code')
        if content is None:
            return jsonify({'error': 'No content provided.'}), 400
        
        file_path = os.path.join(config.STATIC_DIR, payload_name)
        # check if file exists
        if not os.path.isfile(file_path):
            file_path = config.STATIC_DIR + '/' + payload_name
        
        with open(file_path, 'w') as file:
            file.write(content)
        
        return jsonify({'message': 'Code saved successfully.'}), 200
    except Exception as e:
        log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
        return jsonify({'error': 'Failed to save code payload.'}), 500


# inject the generated payload into the target system.
@code_injection_panel.route('/code_injection', methods=["POST"])
def code_injection():
    """
    Inject a code payload into a target system.
    Returns:
        JSON response indicating success or failure of the injection.
    """
    if "email" not in session:
        return jsonify({'error': 'Unauthorized access.'}), 401
    
    db = SessionLocal()
    try:
        data = request.json
        target_name = data.get('target_name')
        payload_name = data.get('payload_name')
        payload = data.get('payload')
        
        targets = getlist(db.query(Targets).filter_by(target_name=target_name).all(), sp=',')
        instraction = getlist(db.query(Instraction).filter_by(target_name=target_name).all(), sp=',')
        
        if len(targets) != 0 and len(instraction) != 0:
            db.query(Instraction).filter_by(
                target_name=target_name,
                status=config.STUTAS[0],  # 'Active'
            ).update({
                'status': config.STUTAS[1]  # 'Inactive'
            }, synchronize_session=False)

            db.query(Instraction).filter_by(
                target_name=target_name,
                instraction=config.INSTRACTION[3]  # 'codeInjection'
            ).update({
                'status': config.STUTAS[0]  # 'Active'
            }, synchronize_session=False)
            
            # Here you would add the logic to inject the payload into the target system.
            # This is a placeholder for demonstration purposes.
            db.add(code_injection_payloads(
                ID=config.ID(10),
                target_name=target_name,
                payload_name=payload_name,
                payload=payload,
                target_staus=config.STUTAS[1],  # 'Inactive'
                user_status=config.CHECK_UPDATE[1]  # 'unchecked'
            ))
            
            db.commit()
            log(f"Injecting payload into target {target_name} for user {session['email']}")
            return jsonify({'message': 'Payload injection initiated.'})
        else:
            return jsonify({'error': 'Target or instruction not found.'}), 404
            
    except Exception as e:
        db.rollback()
        log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
        return jsonify({'error': 'Failed to inject payload.'}), 500
    finally:
        db.close()



@code_injection_panel.route('/code_injection/active_target', methods=["POST", "GET"])
def active_target():
    """
    Activate a target for code injection.
    Returns:
        JSON response indicating success or failure of the activation.
    """
    if "email" not in session:
        return jsonify({'error': 'Unauthorized access.'}), 401
    
    db = SessionLocal()
    try:
        if request.method == 'POST':
            data = request.get_json()
            if not data or 'target_name' not in data:
                return jsonify({'error': 'Target name is required'}), 400
                
            target_name = data['target_name']
            targets = getlist(db.query(Targets).filter_by(target_name=target_name).all(), sp=',')
            instraction = getlist(db.query(Instraction).filter_by(
                target_name=target_name, 
                status=config.STUTAS[1]
            ).all(), sp=',')
            
            print(config.STUTAS[1], instraction)
            if len(targets) != 0 and len(instraction) != 0:
                db.query(Instraction).filter_by(
                    target_name=target_name,
                    instraction=config.INSTRACTION[3],  # 'codeInjection'
                ).update({
                    'status': config.STUTAS[0]  # 'active'
                }, synchronize_session=False)
                
                db.commit()
                log(f"Activating target {target_name} for user {session['email']}")
                return jsonify({'message': 'Target activated.'}), 200
            else:
                return jsonify({'error': 'Target not found.'}), 404
        
        # GET method - get inactive targets
        elif request.method == 'GET':
            # Get all inactive instructions for code injection
            inactive_instructions = db.query(Instraction).filter_by(
                status=config.STUTAS[1],  # 'Inactive'
                instraction=config.INSTRACTION[3]  # 'codeInjection'
            ).all()
            
            inactive_pyload = []
            for inst in inactive_instructions:
                # Check if there are code injection payloads for this target
                inactive_code_injections = db.query(code_injection_payloads).filter_by(
                    user_status=config.CHECK_UPDATE[1],  # 'unchecked'
                    target_staus=config.STUTAS[1],  # 'Inactive'
                    target_name=inst.target_name
                ).all()
                
                if inactive_code_injections:
                    inactive_pyload.append(inst.target_name)

            return jsonify({'inactive_payloads': inactive_pyload})
        
        else:
            return jsonify({'error': 'Invalid request method.'}), 400

    except Exception as e:
        db.rollback()
        log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
        return jsonify({'error': 'Failed to activate target.'}), 500
    finally:
        db.close()


# check if the injected payload has returned an update.
@code_injection_panel.route('/code_injection/check_update', methods=["GET"])
def check_update():
    """
    Check for updates from injected code payloads.
    Returns:
        JSON response indicating whether there are updates or not.
    """
    if "email" not in session:
        return jsonify({'error': 'Unauthorized access.'}), 401
    
    db = SessionLocal()
    try:
        update_code_updated = db.query(code_injection_payloads).filter_by(
            target_staus=config.STUTAS[0],  # "Active" or "Pending" commands
        ).all()
        list_of_update_payloads = getlist(update_code_updated, sp=',')
        if update_code_updated:
            notifcation = {}
            for list_of_update_payload in list_of_update_payloads:
                valid_target = db.query(Targets).filter_by(
                    user_email = session['email'], # user email
                    target_name = list_of_update_payload[3] # target name
                )
                if valid_target:
                    # ID, target_name and payload_name
                    notifcation['info'] = (
                        list_of_update_payload[0], # ID
                        list_of_update_payload[3], # target name
                        list_of_update_payload[1], # payload name
                    )
            return jsonify({
                'status': 'updated',
                'instraction': notifcation,
            })
        else:
            return jsonify({'status': 'notYet'})
    except Exception as e:
        log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
        return jsonify({'error': 'Failed to check for updates.'}), 500
    finally:
        db.close()


@code_injection_panel.route('/code_injection/get_output/<ID>', methods=["GET"])
def get_output(ID):
    """
    Retrieve the output of a specific code injection payload by its ID.
    Args:
        ID (str): The ID of the code injection payload.
    Returns:
        JSON response containing the output or an error message.
    """
    if "email" not in session:
        return jsonify({'error': 'Unauthorized access.'}), 401
    
    db = SessionLocal()
    try:
        code_injection_info_in_db = db.query(code_injection_payloads).filter_by(ID=ID).first()
        
        if not code_injection_info_in_db:
            return jsonify({'error': 'No code injection info found for the given ID.'}), 404
        
        try:
            output = readFromJson('code-output', code_injection_info_in_db.target_name)[code_injection_info_in_db.payload_name][code_injection_info_in_db.ID]
            print('output',output)
        except KeyError:
            output = "No output found."
        except Exception as e:
            log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
            output = "Error retrieving output."

        return jsonify({'outputs': output})
    except Exception as e:
        log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
        return jsonify({'error': 'Failed to retrieve outputs.'}), 500
    finally:
        db.close()