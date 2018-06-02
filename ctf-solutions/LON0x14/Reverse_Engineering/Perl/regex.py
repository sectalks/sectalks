#!/usr/bin/env python

import os
import re
import sys

REGEX_FILE = 'regexp.pl'

password = []

try:
	with open(REGEX_FILE) as file:
		regexes = file.readlines()
except IOError as e:
	sys.exit("Unable to open {}".format(REGEX_FILE))
	
for regex in regexes[::-1]: # Loop through regex lines in reverse
	match = re.search("s/\^\(\.\{(\d+)\}\)([^\(]+)", regex) # Extract chr and pos
	if match: # Only process line if regex matched
		location = int(match.group(1))
		letter = match.group(2)[-1] # Letter may be two chars if escaped with slash
		# Split password at letter location
		start = password[:-location]
		end = password[-location:]
		# Put letter in correct location
		if location == 0:
			password = [letter] + start + end
		else:
			password = end + [letter] + start
		print("".join(password))
				
print "\nTrying password: {}".format("".join(password))
sys.stdout.flush()
os.system("./regexp.pl \"{}\"".format("".join(password)))
