#!/usr/bin/env python3

from pwn import *

r = remote('actf.xyz', 35002)

r.recvline()
r.recvline()

opposites = {
    "False": "True",
    "Left": "Right",
    "Up": "Down",
    "North": "South",
    "Yes": "No",
    "West": "East",
    "In": "Out",
}
rev = {v: k for k, v in opposites.items()}
opposites.update(rev)
print(opposites)

while True:
    chal = r.recvline()
    print(chal)

    for k, v in opposites.items():
        if (k+"?").encode('ascii') in chal:
            r.sendline(v)
