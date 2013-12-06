#!/usr/bin/python
#breakdict.py
import sys
brute = open("all.lst", "r")
words = []
for line in brute:
    words.append(line.strip())
print('\nread in done\n')
z = 0
for z in range(z, len(words)):
    passcode = 1
    usercode = 1
    usertot = 0
    passtot = 0
    username = words[z]
    password = words[z]
    for i, c in enumerate(password):      
        passtot += (i*ord(c)*ord(c))
        passcode *= ord(c)
    for i, c in enumerate(username):
        usertot += (i*ord(c))
        usercode *= ord(c)    
    if  usercode == 1172188274400:
        print('\n\nUsername: '+username)
    if usertot == 1537:
        print('\n\nUsername: '+username)
    if passcode == 1842055687879732800:
        print('\n\nPassword: '+password)
    if passtot == 393644:
        print('\n\nPassword: '+password)
print('done')