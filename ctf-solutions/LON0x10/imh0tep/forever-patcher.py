#!/usr/bin/env python3

import os

with open('./forever-linux', 'rb') as f:
    forever = bytearray(f.read())
    forever[2791] = 0x00 # Patch `cmp BYTE PTR [rbp-0x9],0x1` to `cmp BYTE PTR [rbp-0x9],0x0`
    forever[3103] = 0x75 # Patch `je 0x400c4f <main+388>` to `jne 0x400c4f <main+388>`
    forever[2670] = 0x74 # Patch `jne 0x400a89 <THE_FINAL_COUNTDOWN+81>` to `je 0x400a89 <THE_FINAL_COUNTDOWN+81>`
    with open('./forever-linux-patched', 'wb') as f2:
        f2.write(forever)
        os.chmod('./forever-linux-patched', 0o755)