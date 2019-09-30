import re
import socket

OPPOSITES = {}


def add_pair(a, b):
    OPPOSITES[a] = b
    OPPOSITES[b] = a


add_pair("Up", "Down")
add_pair("Right", "Left")
add_pair("North", "South")
add_pair("East", "West")
add_pair("In", "Out")
add_pair("No", "Yes")
add_pair("True", "False")


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("connecting")
socket.connect(('actf.xyz', 35002))
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


for line in readlines(socket):
    print(line)
    if b'?' not in line:
        continue
    q = line[line.find(b'.') + 2:-1]
    print("Want opposite of", q)
    ans = OPPOSITES[q.decode()].encode()
    print("Answer is", ans)
    socket.send(b"%s\n" % ans)
