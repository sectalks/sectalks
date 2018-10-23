#!/usr/bin/env python3
 
import sys
import socket
from pexpect import fdpexpect
 
abc = b'abcdefghijklmnopqrstuvwxyz '
 
if len(sys.argv) > 2:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((sys.argv[1], int(sys.argv[2])))
    session = fdpexpect.fdspawn(s.fileno(), timeout=10)
    
    session.expect('normal letters back.')
    session.send(abc+b'\n')
    session.expect('.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n')
    
    alphabet = session.match.group(0).strip().split(b'\n')
    fingerprints = [b''] * len(abc)
    for line in alphabet:
        for i in range(len(abc)):
            fingerprints[i] += line[i+8*i:(i+8*i)+8]

    while True:
        e = session.expect(['(.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n)De-asciinate those letters...', 'STL{.*?}'])
        
        if e == 0:
            deascii = session.match.group(1).strip().split(b'\n')
            results = [b''] * (len(deascii[0])//8)
            for line in deascii:
                for i in range(len(deascii[0])//8):
                    results[i] += line[i+8*i:(i+8*i)+8]
         
            res = ''
            for r in results:
                for i, f in enumerate(fingerprints):
                    if r.startswith(f):
                        res += chr(abc[i])
                        break
         
            print('sending {}'.format(res))
            session.send(res.encode()+b'\n')
            
            session.expect('Thanks for asciinating!')
        else:
            print(session.after.decode())
            break