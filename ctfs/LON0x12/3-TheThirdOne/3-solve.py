#!/usr/bin/env python3

from PIL import Image
import re

img = Image.open('now_what.png')
w, h = img.size
msg = ''
for y in range(w):
    for x in range(h):
        r, g, b = img.getpixel((y, x))
        msg += chr(r+b+g)

m = re.search('STL{.*?}', msg)
if m:
    print(m.group(0))