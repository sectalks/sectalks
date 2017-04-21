#!/usr/bin/python
from PIL import Image
import sys
import binascii
import cStringIO
import base64

# To create the same challenge:
# python hide.py original.py $(cat jsfuck.js) 'sectalks<3'

if len(sys.argv) < 3:
    raise Exception("Usage: python hide.py <picture> <message> <xor_key>")

picture = sys.argv[1]
message = sys.argv[2]
xor_key = sys.argv[3]

# Convert code to binary, remove the leading '0b'
code_bin = bin(int(binascii.hexlify(message), 16))[2:]
code_bin_len = len(code_bin)

# Open the image and convert to rgb
img = Image.open(picture, 'r')
pixdata = img.load()

current_code_counter = 0
new_data = []

# Clean the background noise, and encode the binary data as a subtle gray difference.
for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):

        # Get the current pixel base
        current_pixel = pixdata[x, y]
        base = (current_pixel[0] + current_pixel[1] + current_pixel[2]) / 3

        if current_code_counter < code_bin_len:

            # Toggled color
            new_base = base

            # We can't add 1 if the new base is 254, in this case, remove 1.
            if new_base == 254:
                new_base == 253
            else:
                new_base += 1

            # Change G for 0, change R for 1
            if code_bin[current_code_counter] == '0':
                new_data.append((base, new_base, base))
            else:
                new_data.append((new_base, base, base))

            current_code_counter += 1
        else:
            new_data.append((base, base, base))

# Replace the existing pixels with the new ones
img.putdata(new_data)

# Save the image to a virtual buffer and convert it to base64
buffer = cStringIO.StringIO()
img.save(buffer, format="png")
img_b64 = base64.b64encode(buffer.getvalue())

#  Add the needed HTML header for inline data
html_img_b64 = 'data:image/png;base64,' + img_b64

# XOR the image string with the first 10 chars of the key
xored_array = [
    ord(html_img_b64[i]) ^ ord(xor_key[i%10])
    for i in xrange(len(html_img_b64))
]

# Build the HTML payload to inject the data into
html_template = ";".join([
        "<body onload=\"a=String.fromCharCode",
        "String.prototype.b=String.prototype.charCodeAt",
        "Number.prototype.c=Number.prototype.toString",
        "key=prompt('Enter the key')",
        "document.body.innerHTML='<img src='+{}.map((e,i)=>a(e^key[i%10].b(0).c(10))).join('')+' />'",
        "\"></body>"
])

# Save the HTML document
with open('challenge.html', 'w') as result:
    result.write(html_template.format(str(xored_array)))

# Image debug
#  img.save('b64_' + picture)
