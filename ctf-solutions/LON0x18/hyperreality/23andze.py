#!/usr/bin/python3

import binascii
import zlib
import re

with open('pcap3.pcap', 'rb') as f:
    pcap = binascii.hexlify(f.read()).decode('ascii')

hexes = re.findall("c70001000000(.*?)0a45", pcap)

print(hexes)

out = [0] * len(hexes) * (len(hexes[0]) // 2)
for i, num in enumerate(hexes):
    for j, a in enumerate(re.findall('.{2}', num)):
        out[i + j * len(hexes)] = a

ar = bytearray.fromhex(''.join(out))
print(zlib.decompress(ar))
