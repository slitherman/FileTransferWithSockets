import socket
import tqdm
import os
from cryptography.fernet import Fernet

def load_key():
    """
    Loads the key from the current directory named `key.key`
    """
    return open("key.key", "rb").read()

# device's IP address
#ip acceps any incomming connection
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ADDRESS = (SERVER_HOST,SERVER_PORT)
s.bind(ADDRESS)
s.listen(10)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
# accept connection if there is any
client_socket, address = s.accept()
print(f"[+] {address} is connected.")
# receive the file infos
# receive using client socket, not server socket
received = client_socket.recv(BUFFER_SIZE).decode()
encrypted_filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
encrypted_filename = os.path.basename(encrypted_filename)

key = load_key()
f = Fernet(key)
filename = f.decrypt(encrypted_filename.encode()).decode()

# convert to integer
filesize = int(filesize)
# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

# close the client socket
client_socket.close()
# close the server socket
s.close()
