"""
Finds where David lives, then finds all locations in that area. Turns out there's only one user with locations in that
area, so there's a likely chance it is David.

Look at the 2 matching locations on Google Maps and see what's there.

> python3 chal6.py
OrderedDict([('SSN', '305-37-8267'), ('Name', 'David Dreier'), ('Home Address', '3 Santa Cruz Street, Laguna Beach, CA 92651'), ('Job Occupation', 'Politican'), ('Phone No', '001-402-445-5175'), ('Condition', 'Toothache')])
[OrderedDict([('user_id', 'ef1691441b0e'), ('lat', '33.532699'), ('long', '-117.769421')]), OrderedDict([('user_id', 'ef1691441b0e'), ('lat', '33.531554'), ('long', '-117.774201')])]
https://www.google.com/maps/place/33.532699,-117.769421/@33.532699,-117.769421,21z/
https://www.google.com/maps/place/33.531554,-117.774201/@33.531554,-117.774201,21z/

Answer -

mainstreet-bar.com
"""

import csv


with open('chal6.csv') as f:
    data = list(csv.DictReader(f))

with open('chal6locations.csv') as f:
    location_data = list(csv.DictReader(f))

david_dreier = [d for d in data if d['Name'] == 'David Dreier'][0]
print(david_dreier)

# looks like he lives in Laguna Beach
# which of the locations correspond to Laguna Beach (https://www.google.com/maps/place/Laguna+Beach,+CA,+USA/)?
# rough bounding box - SW (33.485107, -117.822536), NE (33.614743, -117.728364)
southwest_corner = (33.485107, -117.822536)
northeast_corner = (33.614743, -117.728364)
min_lat, max_lat = southwest_corner[0], northeast_corner[0]
min_long, max_long = southwest_corner[1], northeast_corner[1]
locations_in_laguna_beach = []
for d in location_data:
    if min_lat <= float(d['lat']) <= max_lat and min_long <= float(d['long']) <= max_long:
        locations_in_laguna_beach.append(d)
print(locations_in_laguna_beach)

# let's build some URLs
for d in locations_in_laguna_beach:
    print(f"https://www.google.com/maps/place/{d['lat']},{d['long']}/@{d['lat']},{d['long']},21z/")
