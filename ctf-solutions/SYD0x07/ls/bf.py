"""
Brute force solution for the SecTalks SYD0x07 first challenge.  
ls@moar.so 2015-05-23
"""

import pexpect  # pexpect is slow, but it's easy to code with and works well for CTFs.
import re
import sys

child = pexpect.spawn('./safe')
child.expect('...\r\n')  # Skip the first line printed to STDOUT.

print 'w00t, and we\'re off!'

combination = ''
count = 0
turn_left = True

# Don't forget to use pexpect.expect_list and precompiled regular expressions for better performance.
patterns = [re.compile('\.'), re.compile('Click!'), re.compile('Safe cracked!'), re.compile('Time\'s up...'), re.compile('Nope...')]

while True:
  if turn_left:
    child.sendline('L')
  else:
    child.sendline('R')
  count += 1
  index = child.expect(patterns)
  if index == 1:
    combination += 'L' * count if turn_left else 'R' * count
    print 'Chaaannngeee direction!'
    count = 0
    turn_left = turn_left ^ True
  elif index == 2:
    combination += 'L' * count if turn_left else 'R' * count
    print 'Success! Write this into a file (e.g. combination) and then pipe it into the binary (e.g. ./safe < combination).'
    print combination[:-1]
    break
  elif index == 3:
    sys.exit('Timeout?!')  # Did you forget to patch the timeout in the binary?
  elif index == 4:
    sys.exit('Nope! Damn.')
