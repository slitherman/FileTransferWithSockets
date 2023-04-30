import socket
import tqdm
import os
from cryptography.fernet import Fernet


def write_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    """
    Loads the key from the current directory named `key.key`
    """
    return open("key.key", "rb").read()


write_key()
key = load_key()

SEPARATOR = "<SEPARATOR>"
encoder = "utf-8"
BUFFER_SIZE = 4096  # send 4096 bytes each time step
# the ip address or hostname of the server, the receiver
host = "192.168.0.199"
# the port, let's use 5001
port = 5001
# the name of file we want to send, make sure it exists
filename = "C:\\Texts\\Hello.txt"

# encrypt the file content
with open(filename, "rb") as f:
    file_data = f.read()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(file_data)

filesize = len(encrypted_data)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")
try:
    s.send(f"{filename}{SEPARATOR}{filesize}".encode(encoder))
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    # send the encrypted file data
    s.sendall(encrypted_data)
    # update the progress bar
    progress.update(filesize)
finally:
    # close the socket in any case
    s.close()
