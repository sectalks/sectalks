#!/usr/bin/env python3

import pexpect

for i in range(10000000,100000000):
    child = pexpect.spawn('./forever-linux')
    child.expect('Enter activation code \[XXXXXXXX\]:')
    child.sendline(str(i))
    index = child.expect(['Activation failed.', pexpect.EOF])
    if index == 1:
        print(i, hex(i), bin(i))