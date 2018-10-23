#!/usr/bin/python2

from pwn import *

r = remote("imhotepisinvisible.com", 6002)

# Skip the banner
r.recvuntil("I needs some proofs of work.")
r.recvline()

while True:
    task = r.recvline()
    print(task)

    start = task.split()[6].replace(',', '').strip()
    length = int(task.split()[9].replace(',', '').strip())
    end = task.split()[-1].replace('.', '').strip()
    print(start)
    print(length)
    print(end)

    cmd = ['./permuter', start, end]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    for line in process.stdout:
        answer = line.strip()

    print(answer)

    r.sendline(answer)
    print(r.recvline())
