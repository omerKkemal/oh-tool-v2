import smtplib
import json
import os
from email.message import EmailMessage
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

def sendEmail(subject,body,to):
    msg = EmailMessage()
    msg.add_alternative(body,subtype=config.EMAIL_TYPE)
    msg['Subject'] = subject
    msg['To'] = to
    msg['From'] = config.EMAIL

    with smtplib.SMTP(config.SMTP_LINK,config.SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(config.EMAIL,config.EMAIL_PASSWORD)

        smtp.send_message(msg)


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

def readFromJson():
    """
    Reads data from the `memory.json` file and returns it as two formats:
    - A `SimpleNamespace` object for easier attribute-based access.
    - A raw Python dictionary (from JSON).

    Returns:
        - `data` (dict): The original dictionary representing the raw data from the JSON file.
    """
    with open(config.JSON_FILE_PATH, 'r') as file:
        data = json.load(file)  # Read the raw data as a Python dictionary
    
    return data


def _load_json():
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
    with open(config.JSON_FILE_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def update_output(target_name, command, result):
    data = _load_json()
    data.setdefault("output", {})
    data["output"].setdefault(target_name, {})
    data["output"][target_name][command] = result
    _save_json(data)

def update_user_info(user_email, status):
    data = _load_json()
    data.setdefault("user-info", {})
    data["user-info"][user_email] = {"stute": status}
    _save_json(data)

def update_target_info(target_name, ip, os_type):
    data = _load_json()
    data.setdefault("target-info", {})
    data["target-info"][target_name] = {
        "ip": ip,
        "os": os_type
    }
    _save_json(data)

def delete_data(subSection, ID, section='output'):
    data = _load_json()
    data.setdefault(section, {})
    if data[section][subSection][ID]:
        del data[section][subSection][ID]
        _save_json(data)
        return 'Done!'
    
    return 'Faild'