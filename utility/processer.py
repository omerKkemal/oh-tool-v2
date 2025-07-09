# -*- coding: utf-8 -*-
"""SpecterPanel - Utility Functions
This module provides utility functions for the SpecterPanel application.
These functions include:
- getlist: Processes a list of SQLAlchemy model objects and extracts relevant string information.
- sendEmail: Sends an email with a specified subject and body to a given recipient.
- log: Records an event in the application log file with a timestamp.
- readFromJson: Reads data from the `memory.json` file and returns it as a dictionary.
- update_output: Updates the output section in the JSON file for a specific target and command.
- update_socket_info: Updates the socket-stutas section in the JSON file for a specific socket.
- update_user_info: Updates the user-info section in the JSON file for a specific user.
- update_target_info: Updates the target-info section in the JSON file for a specific target.
- delete_data: Deletes a specific entry from a subsection in the JSON file.
"""

import json
import os
from datetime import datetime
import filelock

from utility.setting import Setting




config = Setting()
config.setting_var()

def getlist(s,sp):
    """
    Processes a list of SQLAlchemy model objects, extracting relevant string
    information and splitting the string into a structured list of values.

    Args:
        s (list): List of SQLAlchemy model instances

    Returns:
        list: A list of lists, where each sublist contains strings parsed from the object string representations.
    """
    _filter = [str(info)[1:-1].split(sp) for info in s]  # Split the string by 'sp' and store it in a list
    # print(_filter)
    return _filter


def log(event):
    """
        Records an event in the application log file with a timestamp.
        The event is appended to a log file with a date and time when it occurred.

        A file lock is used to prevent simultaneous access to the log file, ensuring
        thread safety when logging events.

        Args:
            event (str): The event message that describes the action or occurrence.
    """
    # Use file lock to prevent concurrent access to the log file
    lock = filelock.FileLock('counter.lock')
    event_rec = datetime.now()  # Capture the current timestamp

    with lock:
        # Open the log file in append mode and write the event with timestamp
        with open(config.LOG_DIR + config.LOG_FILE_NAME, "a") as f:
            f.write(f"[  {str(event_rec)}  ] : {str(event)}\n")

def readFromJson(section,sebSection):
    """
    Reads data from the `memory.json` file and returns it as two formats:
    - A `SimpleNamespace` object for easier attribute-based access.
    - A raw Python dictionary (from JSON).

    Returns:
        - `data` (dict): The original dictionary representing the raw data from the JSON file.
    """
    with open(config.JSON_FILE_PATH, 'r') as file:
        data = json.load(file)  # Read the raw data as a Python dictionary
    if len(data[section]) != 0:
        return data[section][sebSection]
    return data.setdefault("socket-stutas", {})


def _load_json():
    """
    Loads JSON data from the application's JSON file.
    If the file does not exist or is invalid, returns a default structure.

    Returns:
        dict: The loaded or default JSON data.
    """
    if not os.path.exists(config.JSON_FILE_PATH):
        return {
            "output": {},
            "user-info": {},
            "target-info": {}
        }
    with open(config.JSON_FILE_PATH, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {
                "output": {},
                "user-info": {},
                "target-info": {}
            }

def _save_json(data):
    """
    Saves the provided data dictionary to the application's JSON file.

    Args:
        data (dict): The data to be saved.
    """
    with open(config.JSON_FILE_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def update_output(target_name, command, result):
    """
    Updates the output section in the JSON file for a specific target and command.

    Args:
        target_name (str): The name of the target.
        command (str): The command identifier.
        result (str): The result/output of the command.
    """
    data = _load_json()
    data.setdefault("output", {})
    data["output"].setdefault(target_name, {})
    data["output"][target_name][command] = result
    _save_json(data)


def update_code_output(target_name, code_output):
    """
    Updates the output section in the JSON file for a specific target and code_output.

    Args:
        target_name (str): The name of the target.
        code_output (str): The code_output identifier.
    """
    data = _load_json()
    data.setdefault("code-output", {})
    data["code-output"].setdefault(target_name, {})
    data["code-output"][target_name] = code_output
    _save_json(data)


def update_socket_info(token, status):
    """
    Updates the socket-stutas section in the JSON file for a specific socket.

    Args:
        token (str): The user's Api token.
        status (str): The status to set for the socket.
    """
    data = _load_json()
    data.setdefault("socket-stutas", {})
    data["socket-stutas"][token] = {"stute": status}
    _save_json(data)



def update_user_info(user_email, status):
    """
    Updates the user-info section in the JSON file for a specific user.

    Args:
        user_email (str): The user's email address.
        status (str): The status to set for the user.
    """
    data = _load_json()
    data.setdefault("user-info", {})
    data["user-info"][user_email] = {"stute": status}
    _save_json(data)

def update_target_info(target_name, ip, os_type):
    """
    Updates the target-info section in the JSON file for a specific target.

    Args:
        target_name (str): The name of the target.
        ip (str): The IP address of the target.
        os_type (str): The operating system type of the target.
    """
    data = _load_json()
    data.setdefault("target-info", {})
    data["target-info"][target_name] = {
        "ip": ip,
        "os": os_type
    }
    _save_json(data)

def delete_data(subSection, ID, section='output'):
    """
    Deletes a specific entry from a subsection in the JSON file.

    Args:
        subSection (str): The subsection name (e.g., target name).
        ID (str): The identifier to delete within the subsection.
        section (str, optional): The main section in the JSON file. Defaults to 'output'.

    Returns:
        str: 'Done!' if deletion was successful, otherwise 'Faild'.
    """
    data = _load_json()
    data.setdefault(section, {})
    if data[section][subSection][ID]:
        del data[section][subSection][ID]
        _save_json(data)
        return 'Done!'
    
    return 'Faild'