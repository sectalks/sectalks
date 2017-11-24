img = bytearray(open('encrypted_image.gif.xored', 'rb').read())

crib = 'GIF89a'

key_prefix = ''.join([chr(img[i] ^ ord(c)) for i, c in enumerate(crib)])
print(key_prefix)

with open('websters', 'r') as dic:
    for word in dic:
        if word.startswith(key_prefix):
            key = word.strip()

# After a lot of faffing around, key turns out to be 'pestproof' (not 'pestprawn')
print(key)

xord_byte_array = bytearray([img[i] ^ ord(key[i % len(key)]) for i in range(len(img))])

with open('out.gif', 'w') as newFile:
    newFile.write(xord_byte_array)

print("Wrote out.gif")

