import struct

chars = [26220, 24935, 31591, 25966, 26979, 30060, 24946, 24429, 28526, 24932, 26979, 24432, 27745, 28259, 26733, 25966, 29821]

out = []
for c in chars:
    a = struct.pack('>H', c)
    out.append(a.decode('ascii'))

print(''.join(out))
