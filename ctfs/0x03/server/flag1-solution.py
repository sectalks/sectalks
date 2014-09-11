#!/usr/bin/python
#
# Sample solution for Flag #1
# This script brutefrces the six-byte alphabetic ARC4 key
#
# - The server responds with a series of bytes directly after a message stating
#   "cipherchange" and "cipher=ARC4:keylen=6:charset=alpha"
# - From this you are expected to guess that you ned to try and brueforce the
#   bytes given using ARC4 and a key length of six, with the alphabet a-z,
#   looking for printable ASCII bytes
# - This will yeild the cleartext string "Invalid Password" for the key "murphy"
# - Login with any username and "murphy" to get the flag.
# 
#   --blinken 

f="""
Patricks-MacBook-Pro:0x03 patrick$ bash -c 'sleep 1; echo blinken; sleep 1; echo test' | nc 54.146.22.247 4445 | hexdump -C
00000000  57 65 4c 63 4f 6d 45 20  74 6f 20 4e 53 41 20 54  |WeLcOmE to NSA T|
00000010  65 6c 65 70 72 65 73 65  6e 63 65 0d 0a 52 65 6d  |elepresence..Rem|
00000020  65 6d 62 65 72 2c 20 69  66 20 79 6f 75 20 64 69  |ember, if you di|
00000030  65 20 69 6e 20 74 68 65  20 67 61 6d 65 2c 20 79  |e in the game, y|
00000040  6f 75 20 64 69 65 20 69  6e 20 72 65 61 6c 20 6c  |ou die in real l|
00000050  69 66 65 0d 0a 0d 0a 52  65 70 65 61 74 65 64 20  |ife....Repeated |
00000060  61 75 74 68 65 6e 74 69  63 61 74 69 6f 6e 20 66  |authentication f|
00000070  61 69 6c 75 72 65 73 20  77 69 6c 6c 20 72 65 73  |ailures will res|
00000080  75 6c 74 20 69 6e 20 64  65 70 6c 6f 79 6d 65 6e  |ult in deploymen|
00000090  74 20 6f 66 20 74 61 63  74 69 63 61 6c 20 72 65  |t of tactical re|
000000a0  73 70 6f 6e 73 65 2e 0d  0a 0d 0a 45 6e 74 65 72  |sponse.....Enter|
000000b0  20 79 6f 75 72 20 75 73  65 72 6e 61 6d 65 0d 0a  | your username..|
000000c0  45 6e 74 65 72 20 79 6f  75 72 20 70 61 73 73 77  |Enter your passw|
000000d0  6f 72 64 0d 0a 63 69 70  68 65 72 63 68 61 6e 67  |ord..cipherchang|
000000e0  65 3a 63 69 70 68 65 72  3d 41 52 43 34 3a 6b 65  |e:cipher=ARC4:ke|
000000f0  79 6c 65 6e 3d 36 3a 63  68 61 72 73 65 74 3d 61  |ylen=6:charset=a|
00000100  6c 70 68 61 0d 0a a7 bc  d0 9f c8 eb 6c 0d d5 96  |lpha........l...|
00000110  c6 ea fd f5 3b 65 0c ac  65 72 72 6f 72 3a 3a     |....;e..error::|
0000011f
Patricks-MacBook-Pro:0x03 patrick$
"""

# From output above - bytes between 'alpha\r\n' and 'error::'
ciphertext = "\xa7\xbc\xd0\x9f\xc8\xeb\x6c\x0d\xd5\x96\xc6\xea\xfd\xf5\x3b\x65\x0c\xac"

# so generator wow
def keylist(n):
	if n == 0:
		yield ""
	else:
		for c in "abcdefghijlkmnopqrstuvwxyz":
			for d in keylist(n-1):
				yield c+d

from Crypto.Cipher import ARC4

counter = 0
for i in keylist(6): # such effishant
	counter += 1
	if counter % 100000 == 0:
		print "%d %s" % (counter, i)
	a = ARC4.new(i)
	b = a.decrypt(ciphertext)
	if all(x.isalpha() or x.isspace() for x in b):
		# such success
		# wow
		print "%s %s" % (i, b)
		raise SystemExit

