# Hint: mp3s tend to contain areas of silence
# And silence is encoded as the same byte repeated
# So if we XOR with a repeated key, it cancels out that byte
# And gives us the actual key

img = bytearray(open('sayflag.mp3.enc', 'rb').read())

with open('bla', 'w') as f:
    for i in range(255):
        crib = bytearray(chr(i) * len(img))
        xord = ''.join(chr(img[i] ^ c) for i, c in enumerate(crib))
        f.write(xord)

# strings -n 20 this file and find the key!

key = "rocheted_commodity_thievable"
print(key)

xord_byte_array = bytearray(img[i] ^ ord(key[i % len(key)]) for i in range(len(img)))

with open('out.mp3', 'wb') as out:
    out.write(xord_byte_array)
