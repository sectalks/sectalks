#!/usr/bin/python
import sys

out = ""
for i in "abcdefghijklmnopqrstuvwxyz":
	if int(sys.argv[1]) % ord(i) == 0:
		out += i

print out
