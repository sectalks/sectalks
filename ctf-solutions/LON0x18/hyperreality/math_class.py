#!/usr/bin/python2

from __future__ import division
from pwn import *

r = remote("imhotepisinvisible.com", 6003)

r.recvuntil("Are you ready for some maths?")
r.recvline()

while True:
    task = r.recvline()
    print(task)

    operation = task.split()[0]
    num1 = task.split()[1]
    num2 = task.split()[3]

    if operation == "add":
        operation = '+'
    if operation == "subtract":
        operation = '-'
        num1, num2 = num2, num1
    if operation == "divide":
        operation = '/'
    if operation == "multiply":
        operation = '*'

    c = eval(num1 + operation + num2)
    result = str(round(c, 8))

    print(result)

    r.sendline(result)
    print(r.recvline())
