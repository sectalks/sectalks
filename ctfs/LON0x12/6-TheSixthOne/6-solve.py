#!/usr/bin/env python3

from PIL import Image
import re

img = Image.open('now_what.gif')
w, h = img.size
msg = ''
char = ''
i = 0
for x in range(0, w, 7):
    for y in range(0, h, 7):
        char += str(img.getpixel((x, y)))
        if i % 7 == 6:
            msg += chr(int(char,2))
            char = ''
        i += 1

m = re.search('STL{.*?}', msg)
if m:
    print(m.group(0))