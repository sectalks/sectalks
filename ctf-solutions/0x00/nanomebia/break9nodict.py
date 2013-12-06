#!/usr/bin/python
#break9nodict.py
import sys
import itertools
from string import ascii_lowercase
chars = ascii_lowercase
for i in itertools.product(chars,repeat=9):
    passcode = 1
    passtot = 0
    password = ''.join(i)
    for i, c in enumerate(password):
        passtot += (i*ord(c)*ord(c))
        passcode *= ord(c)
    if  ((passcode == 1842055687879732800) and (passtot == 393644)):
        f=open("break9nodict-output.txt", "a")
        f.write(password+'\n')
        f.close()
        print('\n\nPassword: '+password)
print('done')