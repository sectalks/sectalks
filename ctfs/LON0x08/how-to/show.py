from PIL import Image
import sys
import binascii

if len(sys.argv) < 2:
    raise Exception("Usage: python hide.py picture")

picture = sys.argv[1]

# open the image and convert to rgb
img = Image.open(picture, 'r')
img = img.convert("RGB")
pixdata = img.load()

bin_code = ""

# Clean the background noise, if color != white, then set to black.
for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pixdata[x, y][0] == pixdata[x, y][1] == pixdata[x, y][2]:
            break
        else:
            if pixdata[x, y][0] != pixdata[x, y][2]:
                bin_code += '1'
            else:
                bin_code += '0'

# convert binary to code, add the leading '0b'
bin_code = int('0b' + bin_code, 2)
print binascii.unhexlify('%x' % bin_code)
