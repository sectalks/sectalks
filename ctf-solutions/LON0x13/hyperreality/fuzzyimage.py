print ''.join(chr(ord(l)+1) for l in "ekfwnq-omf")

with open('ekfwnq-omf') as f:
    a=bytearray(f.read())

with open('Example.png') as f:
    png=bytearray(f.read())

print ''.join(chr(m ^ b) for m,b in zip(png[:30],a))
print ''.join(chr(m ^ b) for m,b in zip(png[-20:],a[-20:]))

key = "dialoguecomprehensiveconstruct"

output = ''.join(chr(c ^ ord(key[i%len(key)])) for i, c in enumerate(a))

with open('out.png', 'w') as f:
    f.write(output)

print "wrote out.png"

