"""
Probably easier to just open up chal1.csv and press cmd/ctrl-f

> python3 chal1.py
OrderedDict([('SSN', '127-84-5616'), ('Name', 'Taylor Swift'), ('Home Address', '7365 Jessica Pike, Nicolechester, AL 40369'), ('Job Occupation', 'Singer'), ('Phone No', '+1-119-017-7294x51917'), ('Condition', 'Norovirus')])

Answer -

Norovirus
"""

import csv

with open('chal1.csv') as f:
    data = list(csv.DictReader(f))

for d in data:
    if d['Name'] == 'Taylor Swift':
        print(d)
