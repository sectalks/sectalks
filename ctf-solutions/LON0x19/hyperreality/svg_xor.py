img = bytearray(open('pic.svg.enc', 'rb').read())

crib = '<?xml version="1.0" encoding="UTF-8"'

key_prefix = ''.join(chr(img[i] ^ ord(c)) for i, c in enumerate(crib))
print(key_prefix)

key = "deuteride_subsistent_myxosarcoma"
print(key)

xord_byte_array = bytearray(img[i] ^ ord(key[i % len(key)]) for i in range(len(img)))

with open('out.svg', 'wb') as out:
    out.write(xord_byte_array)
