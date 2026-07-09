"""Shared utility helpers for processing and system integration."""

import socket

from gunicorn.config import Config
from utility.processer import log

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m'

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DEGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def send_data(client, data):
    pass


def recive_data(client):
    pass


def helper():
    help_text = f"""
        {YELLOW}Enhanced GhostTrigger Commands:{END}

        {GREEN}Core Commands:{END}
        l-host <command>     Execute command on local machine
        download <file>      Download file from remote host  
        server <IP:PORT>     Start server on remote host
        target-ip           Show target IP address
        output_save [True|False] Enable/disable output logging
        help                Show this help message

        {GREEN}Network Commands:{END}
        port-scan <host>    Scan for open ports
        udp-flood <target>  UDP flood test (educational)
        ftp-server [port]   Start FTP server

        {GREEN}File Operations:{END}
        get <file>          Download file via FTP
        put <file>          Upload file via FTP
        list                List files via FTP

        {YELLOW}Type any command followed by -h for detailed help{END}
    """
    return help_text


def handle_client(client):
    while True:
        pass