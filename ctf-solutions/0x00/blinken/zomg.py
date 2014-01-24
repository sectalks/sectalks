#!/usr/bin/python
import sys

usersum = 1537
passsum = 393644
userprod = 1172188274400
passprod = 1842055687879732800

userchars = "acdhnuxy"
passchars = "adglorvx"

cachehits = 1
cachemiss = 0
imperfect = 0

cache = {}

maxdepth = 0

class ImperfectFitException(Exception):
	pass

def reset():
	global cachehits, cachemiss, imperfect, cache, maxdepth
	cachehits = 1
	cachemiss = 0
	imperfect = 0
	maxdepth = 0

# Dynamic approach to finding all possible strings that sum to input
def haxortimes(total, depth, user, chars):
	global cachehits, cachemiss, imperfect, cache, maxdepth
	try:
		if cache[total]:
			#print "%d %d Hit cache" % (depth, total)
			cachehits += 1
			return cache[total]
		else:
			raise ImperfectFitException
	except KeyError:
		pass

	if total == 0:
		#print "%d %d Bottom" % (depth, total)
		#cachehits += 1
		return [""]

	if total < 97:
		cache[total] = False
		#print "%d %d Bad fit" % (depth, total)
		imperfect += 1
		raise ImperfectFitException
	
	strings = []
	for i in chars:
		try:
			if user:
				o = ord(i)
			else:
				o = ord(i)*ord(i)

			substrings = haxortimes(total - o*depth, depth+1, user, chars)
		except ImperfectFitException:
			continue

		strings += [i + x for x in substrings]
	
	cache[total] = strings
	if cachehits % 10000 == 0:
		print "%d %d Returning %d strings %d cache items %d cache hits" % (depth, total, len(strings), len(cache), cachehits)
		maxdepth = depth
	cachemiss += 1
	return strings

def mrtimsey(string):
	ret = 1
	for i in string:
		ret *= ord(i)
	
	return ret


if __name__ == "__main__":
	userstrings = haxortimes(int(sys.argv[1]), 0, True, userchars)
	print "user: %d strings calculated" % (len(userstrings))
	print "user: %d cache hits, %d cache misses, %d imperfect strings rejected" % (cachehits, cachemiss, imperfect)

	reset()
	passstrings = haxortimes(int(sys.argv[2]), 0, False, passchars)
	print "pass: %d strings calculated" % (len(passstrings))
	print "pass: %d cache hits, %d cache misses, %d imperfect strings rejected" % (cachehits, cachemiss, imperfect)

	for s in userstrings:
		if mrtimsey(s) == 1172188274400:
			print s,
	print 
	for s in passstrings:
		if mrtimsey(s) == 1842055687879732800:
			print s,

