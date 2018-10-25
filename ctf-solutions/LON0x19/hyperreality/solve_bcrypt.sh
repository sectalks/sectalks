#!/bin/bash

echo {a..z} {A..Z} {0..9} \{ \} _ | tr ' ' '\n' > wordlist.txt
/usr/sbin/john --wordlist=wordlist.txt bcrypt.txt
/usr/sbin/john --show bcrypt.txt | tr -d '\n' | tr -d '?' | tr -d ':'
