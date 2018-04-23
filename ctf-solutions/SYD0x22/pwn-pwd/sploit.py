#!/usr/bin/env python2

from pwn import *

io = remote('54.89.22.85', 10001)
sleep(2)
io.sendline('supe\x07r_s3cret')
print(io.recvall())

