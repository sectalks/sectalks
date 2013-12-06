#!/usr/bin/python
#break6nodict.py
import sys
import itertools
from string import ascii_lowercase
chars = ascii_lowercase
for i in itertools.product(chars,repeat=6):
    usercode = 1
    usertot = 0
    username = ''.join(i)
    for i, c in enumerate(username):      
        usertot += (i*ord(c))
        usercode *= ord(c)
    if  ((usercode == 1172188274400) and (usertot == 1537)):
        f=open("break6nodict-output", "a")
        f.write(username+'\n')
        f.close()
        print('\n\nUsername: '+username)
print('done')

