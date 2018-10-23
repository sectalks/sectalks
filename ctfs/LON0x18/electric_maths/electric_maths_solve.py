#!/usr/bin/env python3
 
import sys
import socket
import string
from pexpect import fdpexpect
from decimal import Decimal
 
if len(sys.argv) > 2:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((sys.argv[1], int(sys.argv[2])))
    session = fdpexpect.fdspawn(s.fileno(), timeout=10)
 
    while True:
        index = session.expect(['multiply (\d*) and (\d*)', 'divide (\d*) by (\d*)', 'add (\d*) and (\d*)', 'subtract (\d*) from (\d*)', "STL{.*?}"])
 
        result = 0    
        if index == 0:
            a = Decimal(session.match.group(1).decode())
            b = Decimal(session.match.group(2).decode())
            result = a * b
        elif index == 1:
            a = Decimal(session.match.group(1).decode())
            b = Decimal(session.match.group(2).decode())
            result = a / b
        elif index == 2:
            a = Decimal(session.match.group(1).decode())
            b = Decimal(session.match.group(2).decode())
            result = a + b
        elif index == 3:
            a = Decimal(session.match.group(1).decode())
            b = Decimal(session.match.group(2).decode())
            result = b - a
        elif index == 4:
            print(session.after.decode())
            break
 
        if result % 1 == 0:
            session.send('{}\n'.format(result))
        else:
            session.send('{}\n'.format(round(result,8)))
 
    s.close()