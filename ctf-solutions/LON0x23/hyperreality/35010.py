#!/usr/bin/env python3

from PIL import Image
from pwn import *
import base64
import pytesseract
import string

r = remote('actf.xyz', 35010)

while True:
    chal = r.recvline()
    print(chal)
    if chal != b'<start>\n':
        r.interactive()
        break

    b64 = r.recvuntil('<end>')
    # print(b64)
    b64 = b64.replace(b'<end>', b'')
    data = base64.b64decode(b64)

    fname = "im.png"
    with open(fname, 'wb') as f:
        f.write(data)

    image = Image.open(fname)
    text = pytesseract.image_to_string(image, config=f"--oem 0 --psm 7 -c tessedit_char_whitelist={string.ascii_uppercase}")

    print(text)

    r.sendline(text)
    r.recvline()
