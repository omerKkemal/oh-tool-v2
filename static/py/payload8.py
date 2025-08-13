import os,platform
with open('C:\\Windows\\Temp\\system_info.txt', 'w') as f:
    f.write(f'Username: {os.getenv("USERNAME")}\n')
    f.write(f'OS: {platform.platform()}\n')
    f.write(f'Hostname: {platform.node()}\n')