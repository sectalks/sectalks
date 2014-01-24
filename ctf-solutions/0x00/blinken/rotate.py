#!/usr/bin/python
# This is more a scratchpad than a script :/

import base64

s = base64.b64decode("FQEPBRAcExcLHxMABhYSEBMFXUZEWAQAFUQNUwERR18DVUFNXVRdRRFbBAdCRAtWBREWCVEFSkFWHREAER0=")

print len(s)

for i in s:
	print ord(i)

#print len(s)/2.0
#print len(s)/3.0
#print len(s)/4.0

s = base64.b64decode("FQEPBRAcExcLHxMABhYSEBMFXUZEWAQAFUQNUwERR18DVUFNXVRdRRFbBAdCRAtWBREWCVEFSkFWHREAER0=")
s = s[:-4]

s += chr(5) #a
s += chr(23) #d
s += chr(25) #m
s += chr(6) #i
s += chr(15) #n

#for i in [54,  22,  25,  10,  12,  6,  22,  6,  16,  21,  12,  18,  0,  16,  18,  1,  16,  1,  29,  8,  16,  10,  11,  13,  24,  27,  28,  22,  28,  2,  17,  1,  29,  27,  24,  27,  26,  7,  16,  15,  1,  5,  17,  29,  30,  16,  27,  17,  16,  0,  10,  0,  3,  10,  19]:
#	s += chr(i)
print base64.b64encode(s)
raise SystemExit

for j in range(40):
	s = base64.b64decode("FQEPBRAcExcLHxMABhYSEBMFXUZEWAQAFUQNUwERR18DVUFNXVRdRRFbBAdCRAtWBREWCVEFSkFWHREAER0=")
	s = s[:-4]
	s += chr(10)
	s += chr(10)
	s += chr(10)
	s += chr(11)
	s += chr(11)
	s += chr(j)
	print base64.b64encode(s)
s += chr(15)
s += chr(12)
s += chr(6)
s += chr(13)
s += chr(5)
s += chr(0)
s += chr(0)
s += chr(11)
s += chr(0)
s += chr(16)
s += chr(4)
s += chr(17)

for i in range(len(s)):
	a = ord(s[i])
	if i==j:
		s = s[:i-1] + chr(a+1) + s[i:]
		break
#print base64.b64encode(s)

#print "FQEPBRAcExcLHxMABhYSEBMFXUZEWAQAFUQNUwERR18DVUFNXVRdRRFbBAdCRAtWBREWCVEFSkFWHREAER0="
#print base64.b64encode(s)
