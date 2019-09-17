"""
All strings in the file were of length 32, and looked like they only contain hex characters, so it was likely these
values were MD5 hashed (128-bits, common hashing algorithm), encoded as hex.

Rainbow tables are precomputed tables, usually of dictionary words and sometimes password leaks, that allow look up of
MD5 values back to the input.

> python3 chal3.py
[OrderedDict([('SSN', '008f9b830c1530002d9769a9ac953511'), ('Name', '82aa0d3ebbe825a5f00450bd45dcde69'), ('Home Address', 'b54b7567d7e4725d8f51c46f49a284b2'), ('Job Occupation', '7d8df5651401daedf08ed4998adcb429'), ('Phone No', '8cc2feb6857c163635f985b812d39a52'), ('Condition', 'd7d2e15fce1d57157dcc4698ff488d84')])]
- took the MD5 value of the condition, d7d2e15fce1d57157dcc4698ff488d84
- googled for "rainbow table md5" and found https://crackstation.net/
- gave it the MD5 and got the answer

Answer -

Flatulence
"""

import csv
import hashlib


with open('chal3.csv') as f:
    data = list(csv.DictReader(f))

mike_pence_md5 = hashlib.md5(b"Mike Pence").hexdigest()

matches = []
for d in data:
    if d['Name'] == mike_pence_md5:
        matches.append(d)

print(matches)

print(f'- took the MD5 value of the condition, {matches[0]["Condition"]}')
print('- googled for "rainbow table md5" and found https://crackstation.net/')
print('- gave it the MD5 and got the answer')
