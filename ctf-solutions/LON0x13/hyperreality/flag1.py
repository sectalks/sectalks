with open('flag1.zip') as f:
    zippy = bytearray(f.read())

fl = zippy.index('FL')
ag = zippy.rindex('AG')

print ''.join(chr(b - a) for a,b in zip(zippy[fl+3:fl+36], zippy[ag+3:ag+36]))
