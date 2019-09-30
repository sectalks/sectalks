"""
> python3 chal2.py
[('Banker', 16)]

Answer -

Banker
"""

from collections import Counter
import csv


with open('chal2.csv') as f:
    data = list(csv.DictReader(f))

cirrhosis_by_occupation = Counter((d['Job Occupation'] for d in data if d['Condition'].lower() == 'cirrhosis'))
print(cirrhosis_by_occupation.most_common(1))
