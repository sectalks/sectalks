"""
Requires the additional data leak to be in a file named leaked_rented_movie_customers.txt.

Looks for Audrey Cooper in the leak - exists, but there's no address. Any flatmates (same address hash)? Yes, and they
exist in the leak.

> python3 chal5.py
[OrderedDict([('Name', 'Audrey Cooper'), ('Address', ''), ('addr_hash', ''), ('Movie', 'Apocalypse Now'), ('movie_hash', 'f877a48d02905f52267b5ca1a7ccb739')])]
[OrderedDict([('SSN', 'ca3dc5833da2bac55df13aee9e064254'), ('Name', 'Cornelia Griggs'), ('Home Address', '17bbb461e7b1f87168907251562d6911'), ('Job Occupation', '98533b5d6c0abec3a805162a5f6b4cfa'), ('Phone No', 'd51c0e345963f853a5972e7e8f1a6a48'), ('Condition', '4703b0725e9b13aece91ddf9c85ef17e')])]
OrderedDict([('Name', 'Cornelia Griggs'), ('Address', '1460 Claridge Drive, Beverly Hills, CA 90210'), ('addr_hash', '17bbb461e7b1f87168907251562d6911'), ('Movie', 'Love Actually'), ('movie_hash', '9b3ab82b87c1a801d03c67a3a83d0234')])

Answer -

Claridge_Drive_90210
"""

import csv


with open('chal5.csv') as f:
    data = list(csv.DictReader(f))

with open('leaked_rented_movie_customers.txt') as f:
    leak = list(csv.DictReader(f))

leak_matches_for_audrey_cooper = [d for d in leak if d['Name'] == 'Audrey Cooper']
print(leak_matches_for_audrey_cooper)

# no address for Audrey Cooper in the leak :(

# How about those who might live at the same address as Audrey Cooper?
audrey_cooper_data = [d for d in data if d['Name'] == 'Audrey Cooper'][0]
audrey_cooper_address_hash = audrey_cooper_data['Home Address']
data_matches_for_audrey_cooper_address_hash = [
    d for d in data if d['Home Address'] == audrey_cooper_address_hash and d['Name'] != 'Audrey Cooper'
]
print(data_matches_for_audrey_cooper_address_hash)

# flatmates found. Are they in the leak?
flatmate_names = {d['Name'] for d in data_matches_for_audrey_cooper_address_hash}
for d in leak:
    if d['Name'] in flatmate_names:
        print(d)
