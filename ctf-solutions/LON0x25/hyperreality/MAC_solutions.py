#!/usr/bin/env python3

from pwn import *

import json
import zlib

REMOTE = "mtg.wtf"
flags = []


def sign(port, msg):
    r = remote(REMOTE, port)
    r.recvuntil("cookie\n")
    r.sendline("sign")
    r.recvuntil("sign:\n")
    r.sendline(msg)

    resp = r.recvline()
    resp = resp.decode().strip().split()[1]
    cookie = json.loads(resp)

    r.close()

    return cookie


def login(port, cookie):
    r = remote(REMOTE, port)
    r.recvuntil("cookie\n")
    r.sendline("login")
    r.recvuntil("cookie:\n")

    r.sendline(json.dumps(cookie))
    print(r.recvline())
    print(r.recvline())
    flag = r.recvline().decode().strip().split()[1]
    flags.append(flag)
    print(flag)

    r.close()


# CRC-32 MAC
port = 9000
cookie = sign(port, "admin")
updated_crc = zlib.crc32(b"=yes", cookie["mac"])
payload = {"msg": "admin=yes", "mac": updated_crc}
login(port, payload)


# Salted MAC
port = 9001
while True:
    cookie = sign(port, "dmin=yes")
    if cookie['salt'].endswith("a"):
        break

cookie['salt'] = cookie['salt'][:-1]
cookie['msg'] = "a" + cookie['msg']

login(port, cookie)


# Poly-DIY MAC
port = 9002
while True:
    cookie1 = sign(port, "\x00")
    cookie2 = sign(port, "\x01")

    if cookie1['nonce'] == cookie2['nonce']:
        break

aes_n = cookie1['mac']
ri = cookie2['mac'] - cookie1['mac']

admin_unpacked = 2128687511491035620449  # admin=yes
prime = 2**130 - 5
# Evaluate polynomial
z = (admin_unpacked * ri) % prime
# Apply nonce
payload_mac = (z + aes_n) % prime

payload = {"msg": "admin=yes", "nonce": cookie1['nonce'], "mac": payload_mac}

login(port, payload)


print(flags)
