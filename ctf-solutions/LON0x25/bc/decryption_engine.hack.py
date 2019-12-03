#!/usr/bin/env python
"""
Decryption Engine
"""

from Crypto.Cipher import AES
from datetime import datetime
import sys

def decrypt(filename, passphrase):
    try:
        cipher_text = open(filename, 'rb').read()
    except IOError:
        print "Error: File does not exist."
        return
    return AES.new(passphrase, AES.MODE_CBC, 'FDK184481HGBBRVS').decrypt(cipher_text)


if __name__ == "__main__":
    for h in range(24):
        for m in range(60):
            res = decrypt(sys.argv[1], 'Current Time: %02d%02d hours' % (h, m))
            if res.startswith('flag{'):
                print(res)
                sys.exit(0)
