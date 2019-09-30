import socket
import subprocess
from base64 import b64decode as b6d

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("connecting")
socket.connect(('actf.xyz', 35010))
print("connected")

def readlines(sock, recv_buffer=4096, delim=b'\n'):
    buffer = b''
    data = True
    while data:
        data = sock.recv(recv_buffer)
        buffer += data

        while buffer.find(delim) != -1:
            line, buffer = buffer.split(b'\n', 1)
            yield line
    return

img = b''
for line in readlines(socket):
    print(">", line)
    if b">" not in line:
        img += line
    elif b'<end>' in line:
        print("img", img)
        with open("out.png", "wb") as f:
            f.write(b6d(img))
        subprocess.run(["/usr/bin/img2txt", "out.png"])
        img = b''
        inp = input().encode()
        print("you said inp", inp)
        socket.send(inp)
