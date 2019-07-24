from fractions import gcd
from functools import reduce
import string

def find_gcd(list):
    x = reduce(gcd, list)
    return x

ppt = bytearray(open('challenge_files/powerpoint_presentation.pptx.enc', 'rb').read())

# it turns out the key can more or less be read from the end of the file due
# to the large number of null bytes in the pptx format
#
# here's a crib-dragging approach anyway

# pptx header
crib = [0x50, 0x4B, 0x03, 0x04, 0x14, 0x00, 0x06, 0x00, 0x08, 0x00, 0x00, 0x00, 0x21, 0x00, 0xDF, 0xCC]

key_prefix = ''.join([chr(ppt[i] ^ c) for i, c in enumerate(crib)])
print(key_prefix)

# only the first 6 chars appear to have worked
key_prefix = key_prefix[:6]
print(key_prefix)

# there's lots of these in the file so lots of alignments
crib2 = "ppt/"

# use the common alignments to figure out the length of the key
factors = []
for i in range(0, len(ppt) - len(key_prefix)):
    sliced = ppt[i:i+len(key_prefix)]
    xord = ''.join([chr(ord(a) ^ b) for a, b in zip(key_prefix, sliced)])

    if crib2 in xord:
        factors.append(i)

key_length = find_gcd(factors)
print("Key length: %s" % key_length)

key = [""] * key_length

# here's a longer string bound to appear in a pptx
crib3 = "ppt/slideLayouts/_rels/slideLayout"

# if we find the key fragment, then probably most of the crib ^ the slice can
# tell us more about the key
for i in range(0, len(ppt) - len(key_prefix)):
    sliced = ppt[i:i+len(crib3)]

    xord = ''.join([chr(ord(a) ^ b) for a, b in zip(crib3, sliced)])
    if key_prefix in xord:
        for j,c in enumerate(xord):
            if c in string.printable:
                key[(i + j) % key_length] = c
        # print(xord)
        print(''.join(key))


key = "somnambulation_hyperrational_unchangingness"

xord_byte_array = bytearray([ppt[i] ^ ord(key[i % len(key)]) for i in range(len(ppt))])

with open('xord.pptx', 'wb') as newFile:
    newFile.write(xord_byte_array)

print("Wrote pptx")
