#!/usr/bin/env python3

import sys
import socket
import string
from pexpect import fdpexpect
import hashlib
import random
from itertools import islice

def random_chars(size, chars=string.ascii_letters):
    selection = iter(lambda: random.choice(chars), object())
    while True:
        yield ''.join(islice(selection, size))

if len(sys.argv) > 2:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((sys.argv[1], int(sys.argv[2])))
    session = fdpexpect.fdspawn(s.fileno(), timeout=10)
    
    while True:
        e = session.expect(['Give me a string starting with (\w*), of length 15, such that its sha1 sum ends in (\w*)\.', 'STL{.*?}'])

        if e == 0:
            start = session.match.group(1)
            end = session.match.group(2)

            random_gen = random_chars(5)
            test = start.decode() + next(random_gen)
            while not hashlib.sha1(test.encode()).hexdigest().endswith(end.decode()):
                test = start.decode() + next(random_gen)
                
            session.send(test+'\n')
        else:
            print(session.after.decode())
            break
            
    s.close()