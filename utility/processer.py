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


# """Top-level smoke tests for the core application workflow."""

# import re

# def clean_top_text(raw_text):
#     """Remove ANSI escape sequences from text."""
#     clean_data = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', raw_text)
#     return clean_data


# # Example usage:
# if __name__ == "__main__":
#     raw_text = """\u001b[?1h\u001b=\u001b[?25l\u001b[H\u001b[2J\u001b(B\u001b[mtop - 13:42:14 up  5:07,  1 user,  load average: 0.70, 0.82, 0.79\u001b(B\u001b[m\u001b[39;49m\u001b(B\u001b[m\u001b[39;49m\u001b[K\nTasks:\u001b(B\u001b[m\u001b[39;49m\u001b[1m 272 \u001b(B\u001b[m\u001b[39;49mtotal,\u001b(B\u001b[m\u001b[39;49m\u001b[1m   1 \u001b(B\u001b[m\u001b[39;49mrunning,\u001b(B\u001b[m\u001b[39;49m\u001b[1m 271 \u001b(B\u001b[m\u001b[39;49msleeping,\u001b(B\u001b[m\u001b[39;49m\u001b[1m   0 \u001b(B\u001b[m\u001b[39;49mstopped,\u001b(B\u001b[m\u001b[39;49m\u001b[1m   0 \u001b(B\u001b[m\u001b[39;49mzombie\u001b(B\u001b[m\u001b[39;49m\u001b(B\u001b[m\u001b[39;49m\u001b[K\n%Cpu(s):\u001b(B\u001b[m\u001b[39;49m\u001b[1m  9.8 \u001b(B\u001b[m\u001b[39;49mus,\u001b(B\u001b[m\u001b[39;49m\u001b[1m  3.9 \u001b(B\u001b[m\u001b[39;49msy,\u001b(B\u001b[m\u001b[39;49m\u001b[1m  0.0 \u001b(B\u001b[m\u001b[39;49mni,\u001b(B\u001b[m\u001b[39;49m\u001b[1m 86.3 \u001b(B\u001b[m\u001b[39;49mid,\u001b(B\u001b[m\u001b[39;49m\u001b[1m  0.0 \u001b(B\u001b[m\u001b[39;49mwa,\u001b(B\u001b[m\u001b[39;49m\u001b[1m  0.0 \u001b(B\u001b[m\u001b[39;49mhi,\u001b(B\u001b[m\u001b[39;49m\u001b[1m  0.0 \u001b(B\u001b[m\u001b[39;49msi,\u001b(B\u001b[m\u001b[39;49m\u001b[1m  0.0 \u001b(B\u001b[m\u001b[39;49mst\u001b(B\u001b[m\u001b[39;49m\u001b(B\u001b[m \u001b(B\u001b[m\u001b[39;49m\u001b(B\u001b[m\u001b[39;49m\u001b[K\nMiB Mem :\u001b(B\u001b[m\u001b[39;49m\u001b[1m   7821.9 \u001b(B\u001b[m\u001b[39;49mtotal,\u001b(B\u001b[m\u001b[39;49m\u001b[1m    495.4 \u001b(B\u001b[m\u001b[39;49mfree,\u001b(B\u001b[m\u001b[39;49m\u001b[1m   4066.0 \u001b(B\u001b[m\u001b[39;49mused,\u001b(B\u001b[m\u001b[39;49m\u001b[1m   4060.4 \u001b(B\u001b[m\u001b[39;49mbuff/cache\u001b(B\u001b[m\u001b[39;49m\u001b(B\u001b[m \u001b(B\u001b[m\u001b[39;49m\u001b(B\u001b[m    \u001b(B\u001b[m\u001b[39;49m\u001b(B\u001b[m\u001b[39;49m\u001b[K\nMiB Swap:\u001b(B\u001b[m\u001b[39;49m\u001b[1m   4096.0 \u001b(B\u001b[m\u001b[39;49mtotal,\u001b(B\u001b[m\u001b[39;49m\u001b[1m   4096.0 \u001b(B\u001b[m\u001b[39;49mfree,\u001b(B\u001b[m\u001b[39;49m\u001b[1m      0.0 \u001b(B\u001b[m\u001b[39;49mused.\u001b(B\u001b[m\u001b[39;49m\u001b[1m   3755.9 \u001b(B\u001b[m\u001b[39;49mavail Mem \u001b(B\u001b[m\u001b[39;49m\u001b(B\u001b[m\u001b[39;49m\u001b[K\n\u001b[K\n\u001b[7m    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND  \u001b(B\u001b[m\u001b[39;49m\u001b[K\n\u001b(B\u001b[m\u001b[1m  12850 omer      20   0   14540   5300   3252 R  23.1   0.1   0:00.06 top      \u001b(B\u001b[m\u001b[39;49m\u001b[K\n\u001b(B\u001b[m   2546 omer       9 -11  118380  16520   9160 S   7.7   0.2   1:51.17 pipewire \u001b(B\u001b[m\u001b[39;49m\u001b[K\n\u001b(B\u001b[m   2791 omer      20   0 4890224 320288 138468 S   7.7   4.0  18:53.02 gnome-s+ \u001b(B\u001b[m\u001b[39;49m\u001b[K\n\u001b(B\u001b[m   9688 omer      20   0 1224.2g 576672 152068 S   7.7   7.2  31:21.51 chrome   \u001b(B\u001b[m\u001b[39;49m\u001b[K\n\u001b(B\u001b[m      1 root      20   0   24328  15440   9416 S   0.0   0.2   0:13.91 systemd  \u001b(B\u001b[m\u001b[39;49m\u001b[K\n\u001b(B\u001b[m      2 root      20   0       0      0      0 S   0.0   0.0   0:00.01 kthreadd \u001b(B\u001b[m\u001b[39;49m\u001b[K\n\u001b(B\u001b[m      3 root      20   0       0      0      0 S   0.0   0.0   0:00.00 pool_wo+ \u001b(B\u001b[m\u001b[39;49m\u001b[K\n\u001b(B\u001b[m      4 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 kworker+ \u001b(B\u001b[m\u001b[39;49m\u001b[K\n\u001b(B\u001b[m      5 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 kworker+ \u001b(B\u001b[m\u001b[39;49m\u001b[K\n\u001b(B\u001b[m      6 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 kworker+ \u001b(B\u001b[m\u001b[39;49m\u001b[K\n\u001b(B\u001b[m      7 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 kworker+ \u001b(B\u001b[m\u001b[39;49m\u001b[K\n\u001b(B\u001b[m      8 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 kworker+ \u001b(B\u001b[m\u001b[39;49m\u001b[K\n\u001b(B\u001b[m     10 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 kworker+ \u001b(B\u001b[m\u001b[39;49m\u001b[K\n\u001b(B\u001b[m     13 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 kworker+ \u001b(B\u001b[m\u001b[39;49m\u001b[K\n\u001b(B\u001b[m     14 root      20   0       0      0      0 I   0.0   0.0   0:00.00 rcu_tas+ \u001b(B\u001b[m\u001b[39;49m\u001b[K\n\u001b(B\u001b[m     15 root      20   0       0      0      0 I   0.0   0.0   0:00.00 rcu_tas+ \u001b(B\u001b[m\u001b[39;49m\u001b[K\n\u001b(B\u001b[m     16 root      20   0       0      0      0 I   0.0   0.0   0:00.00 rcu_tas+ \u001b(B\u001b[m\u001b[39;49m\u001b[K\u001b[?1l\u001b>\u001b[25;1H\n\u001b[?12l\u001b[?25h\u001b[K"""

#     clean = clean_top_text(raw_text)
#     print(clean)


import json
import re
import os
from datetime import datetime
import filelock

from utility.setting import Setting
from utility.email_temp import EmailTemplate




config = Setting()
config.setting_var()



def strip_ansi(text, cmd):
    """Remove ANSI escape sequences from a string."""
    if cmd == 'top':
        # Matches CSI sequences (e.g. \x1b[31m) and other common escape codes
        return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text)
    elif cmd == 'db_info':
        string_format = ''
        for key, value in text[0].items():
            # checke if the value is dict, if it is, convert it to string
            if isinstance(value, dict):
                value = json.dumps(value, indent=4)
                string_format += f"{key}: {value}\n"
            elif isinstance(value, list):
                value = json.dumps(value, indent=4)
                string_format += f"{key}: {value}\n"
            else:
                string_format += f"{key}: {value}\n"
        return string_format
    else:
        return text

def email_optimize(send_to, baseUrl, temp_type, ip=None, os_type=None, target_name=None):
    
    """
    Sends an email using predefined templates based on the specified type.
    Args:
        send_to (str): Recipient email address.
        temp_type (str): Type of email template to use. Options include:
                         'new_user', 'reset_password', 'approved',
                         'rejected', 'target_reached', 'welcome'.
        ip (str, optional): IP address for 'target_reached' template.
        os_type (str, optional): OS type for 'target_reached' template.
        target_name (str, optional): Target name for 'target_reached' template.
    Returns:
        str: Confirmation message indicating the email was sent.
    Raises:
        ValueError: If an invalid template type is specified.
    """
    emailTemplate = EmailTemplate(baseUrl=baseUrl.rstrip('/'))

    templates_to_test = [
        ('Welcome to SpecterPanel', emailTemplate.user_notify(send_to)),
        ('New User Registration Alert', emailTemplate.new_user(send_to)),
        ('Password Reset Request', emailTemplate.reset_password('SP-789-XYZ', send_to)),
        ('Account Approved', emailTemplate.approved(send_to)),
        ('Account Application Status', emailTemplate.rejected(send_to)),
        ('New Target Registration', emailTemplate.target_reached(target_name, ip, os_type, send_to)),
        ('Panding(under review)', emailTemplate.panding_message(send_to))
    ]

    if temp_type == 'new_user':
        subject, body = templates_to_test[1]
        recipient = config.ADMIN_EMAIL
    elif temp_type == 'reset_password':
        subject, body = templates_to_test[2]
        recipient = send_to
    elif temp_type == 'approved':
        subject, body = templates_to_test[3]
        recipient = send_to
    elif temp_type == 'rejected':
        subject, body = templates_to_test[4]
        recipient = send_to
    elif temp_type == 'target_reached':
        subject, body = templates_to_test[5]
        recipient = config.ADMIN_EMAIL
    elif temp_type == 'welcome':
        subject, body = templates_to_test[0]
        recipient = send_to
    elif temp_type == 'panding':
        subject, body = templates_to_test[6]
        recipient = send_to
    else:
        raise ValueError("Invalid template type specified.")

    emailTemplate.send_email(subject, body, recipient)
    return f"Email of type '{temp_type}' sent to {config.ADMIN_EMAIL}."


def clean_ANSI_escape_text(raw_text):
    """Remove ANSI escape sequences and problematic control chars."""
    # Remove ANSI escape sequences
    text = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', raw_text)

    # Remove carriage returns
    text = text.replace('\r', '')

    # Replace tabs with spaces
    text = text.replace('\t', '    ')

    # Remove any non-printable control characters
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)

    return text


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
        with open(config.LOG_FILE_PATH, "a") as f:
            f.write(f"[  {str(event_rec)}  ] : {str(event)}\n")

def readFromJson(section, subSection):
    """
    Reads data from the memory.json file and retrieves specific subsection data.

    Args:
        section (str): The main section key.
        subSection (str): The sub-section key inside the section.

    Returns:
        dict or None: The data from the subSection, or None if not found or error occurs.
    """
    try:
        with open(config.JSON_FILE_PATH, 'r') as file:
            data = json.load(file)

        if section not in data:
            print(f"[!] Section '{section}' not found in JSON.")
            return None

        if subSection not in data[section]:
            print(f"[!] Sub-section '{subSection}' not found under section '{section}'.")
            return None

        return data[section][subSection]

    except FileNotFoundError:
        print(f"[!] JSON file not found: {config.JSON_FILE_PATH}")
    except json.JSONDecodeError:
        print(f"[!] Failed to parse JSON file: {config.JSON_FILE_PATH}")
    except Exception as e:
        print(f"[!] Unexpected error reading JSON: {e}")
    
    return None



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


def update_code_output(target_name, pyload_name, ID, code_output):
    data = _load_json()

    data.setdefault("code-output", {})
    data["code-output"].setdefault(target_name, {})
    data["code-output"][target_name].setdefault(pyload_name, {})

    data["code-output"][target_name][pyload_name][ID] = code_output

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

def delete_data(subSection, ID=None, section='output'):
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
    if ID:
        if data[section][subSection][ID]:
            del data[section][subSection][ID]
            _save_json(data)
            return 'Done!'
    else:
        if subSection in data[section] and data[section][subSection]:
            del data[section][subSection]
            _save_json(data)
            return 'Done!'
        
    return 'Faild'