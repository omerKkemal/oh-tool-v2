import socket
import nmap
import subprocess
import os
import re

def check_file_permissions(filepath):
    """Checks file permissions on the given filepath."""
    try:
        stat_info = os.stat(filepath)
        permissions = stat_info.st_mode
        permissions_str = oct(permissions)[2:].zfill(10)
        print(f"File permissions for {filepath}: {permissions_str}")
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except Exception as e:
        print(f"Error checking permissions for {filepath}: {e}")



def enumerate_services(target_ip):
    """Enumerates services running on the target IP address using nmap."""
    try:
        nm = nmap.PortScanner()
        nm.scan(target_ip, arguments='-sS -p 1-100') #TCP SYN scan, ports 1-100
        print(f"Services detected on {target_ip}:")
        for host in nm.all_hosts():
            for port in nm[host]['tcp']:
                print(f"  Port {port}: {nm[host]['tcp'][port]['state']}")
    except Exception as e:
        print(f"Error during nmap scan: {e}")


def check_sudos(filepath):
    """Checks if a file has sudo privileges."""
    try:
      if os.geteuid() == 0:
          print(f"Sudo privileges checked for {filepath}: Likely available (root).")
      else:
          result = subprocess.run(['sudo', 'id', filepath], capture_output=True, text=True, check=True)
          print(f"Result of sudo id for {filepath}: {result.stdout}")
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except subprocess.CalledProcessError as e:
        print(f"Error checking sudo privileges: {e}")



def check_file_hash(filepath):
    """Calculates and verifies file hashes (MD5, SHA256)."""
    try:
        md5_hash = os.popen("md5sum " + filepath).read().split()[0]
        sha256_hash = os.popen("sha256sum " + filepath).read().split()[0]
        print(f"MD5 hash of {filepath}: {md5_hash}")
        print(f"SHA256 hash of {filepath}: {sha256_hash}")
        if md5_hash == sha256_hash:
             print("MD5 and SHA256 hashes match.")
        else:
            print("MD5 and SHA256 hashes do not match.")

    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except Exception as e:
        print(f"Error calculating hashes: {e}")


def check_for_common_misconfigurations(filepath):
    """Checks for common misconfigurations in a file."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        if re.search(r"password", content, re.IGNORECASE):
           print("Warning: 'password' may be present. Review configuration.")
        if re.search(r"sudo", content, re.IGNORECASE):
           print("Warning: 'sudo' may be present. Review configuration.")

    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except Exception as e:
        print(f"Error checking for misconfigurations: {e}")


def run_command(command):
    """Executes a command and prints its output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(f"Command: {command}")
        print(f"Output:\n{result.stdout}")
        if result.stderr:
            print(f"Error:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        print(f"Output:\n{e.output}")


if __name__ == '__main__':
    # Example usage - replace with your desired targets and files
    # targets = ["192.168.1.1", "localhost", "/etc/passwd"]
    files = ["/etc/shadow", "/tmp/test.txt", "/var/log/syslog"]



    # for target in targets:
    #     print(f"\n--- Checking target: {target} ---")
    #     enumerate_services(target)

    for file in files:
        print(f"\n--- Checking file: {file} ---")
        check_file_permissions(file)
        check_sudos(file)
        check_file_hash(file)
        check_for_common_misconfigurations(file)

    #Example command to run:
    #run_command("ls -l /tmp")