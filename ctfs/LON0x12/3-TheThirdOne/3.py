#!/usr/bin/env python3

from PIL import Image
import random

flag = 'STL{CopperExplainUniteBranch}'

im = Image.new('RGB', (400, 400))
pix = im.load()
for x in range(400):
    for y in range(400):
        # The 'special' column that we'll choose to hide the flag in
        if x == 227:
            if y >= 142 and y < 142 + len(flag):
                n = ord(flag[y-142])
            else:
                # Make the rest of the 'special' column black
                # to provide a slight hint to players
                n = 0
        # Every other column gets random numbers in the printable ascii range
        else:
            n = random.randint(32, 127)
        rgb = []
        # Split n up into three random integers that we'll use as rgb
        for i in range(2):
            r = random.randint(0, n)
            rgb.append(r)
            n -= r
        rgb.append(n)
        pix[x,y] = tuple(rgb)

im.save('now_what.png', 'PNG')