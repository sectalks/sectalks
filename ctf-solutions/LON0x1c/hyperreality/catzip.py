from PIL import Image
import re

image = Image.open('challenge_files/flag.catzip')
w, h = image.size
im = image.load()

out = []

for i in range(21, h, 42):
    for j in range(15, w, 42):
        out.append(im[j, i])

# print(out)

def chunks(l, n):
    return (l[i:i + n] for i in range(0, len(l), n))


bins = ""

for bla in out:
    if bla[0] == 190:
        bins += "0"
    elif bla[0] == 236:
        bins += "1"
    else:
        print("bad")

print(bins)


bytess = bytearray([int(a, 2) for a in re.findall('.{8}', bins)])

import zlib
print(zlib.decompress(bytess, 15+32))

