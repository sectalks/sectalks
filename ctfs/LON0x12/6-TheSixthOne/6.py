#!/usr/bin/env python3

from PIL import Image
import random

flag = 'STL{GeneralEatableEvenAromatic}'
# Encode the flag as bits.  We only need 7 bits to encode ascii
binaryflag = ''.join('{:07b}'.format(ord(x)) for x in flag)

im = Image.new('P', (434, 35))
pix = im.load()
count = 0
# Encode the bits as 7x7 blocks of colors 0xaa38ff or 0xb55b97
for x in range(0, 434, 7):
    for y in range(0, 35, 7):
        if count < len(binaryflag):
            n = int(binaryflag[count])
            count += 1
        else:
            n = random.randint(0, 1)
        for i in range(7):
            for j in range(7):
                pix[x+i,y+j] = n

im.save('now_what.gif', format='gif', optimize=True, palette=b'\xaa\x38\xff\xb5\x5b\x97')