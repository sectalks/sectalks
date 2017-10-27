#!/usr/bin/env/python2

import csv
import math
import random
from faker import Faker
import hashlib
import subprocess
from collections import Counter
fake = Faker()
rand = random.SystemRandom()

with open('diseases.txt') as f:
    DISEASES = [line.strip() for line in f.readlines()]

with open('movies.txt') as f:
    MOVIES = [line.strip() for line in f.readlines()]

COLS = ['SSN', 'Name', 'Address', 'Occupation', 'Phone Number', 'Condition']
MOVIE_COLS = ['Name', 'Address', 'addr_hash', 'Rented Movie', 'movie_hash']
LOCATION_COLS = ['user_id', 'lat', 'long']


def write_challenge(outfile, password, rows, readme, extra_name="", extra_data="", extra_cols=COLS):
    csv_name = outfile + '.csv'
    zip_name = outfile + '.zip'
    readme_name = outfile + 'README.txt'

    rand.shuffle(rows)
    rows.insert(0, COLS)
    with open(csv_name, 'wb') as of:
        wr = csv.writer(of)
        wr.writerows(rows)

    if extra_data:
        rand.shuffle(extra_data)
        extra_data.insert(0, extra_cols)
        with open(extra_name, 'wb') as of:
            wr = csv.writer(of)
            wr.writerows(extra_data)

    with open(readme_name, 'w') as of:
        of.write(readme)

    rc = subprocess.call(
        ['7z', 'a', password, '-y', zip_name, csv_name, readme_name, extra_name])


def fake_address():
    return fake.address().replace('\n', ', ')


def custom_hash(data):
    return hashlib.sha256(data).hexdigest()[::-1][:32]


def make_records(size=1000):
    rows = []
    for i in range(size):
        record = [
            fake.ssn(),
            fake.name(),
            fake_address(),
            fake.job(),
            fake.phone_number(),
            rand.choice(DISEASES)
        ]
        rows.append(record)

    return rows


def make_movie_records(size=1000):
    rows = []
    for i in range(size):
        addr = fake_address()
        movie = rand.choice(MOVIES)
        record = [
            fake.name(),
            addr,
            custom_hash(addr),
            movie,
            custom_hash(movie)
        ]
        rows.append(record)

    return rows


def most_common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]


def random_id():
    return ('%012x' % random.randrange(16**12)).lower()


def random_lats_longs(lat, lon, num_rows, random_id):
    out = []
    for _ in xrange(num_rows):
        dec_lat = random.random() / 5
        dec_lon = random.random() / 5
        out.append([random_id, float("{0:.6f}".format(
            lon + dec_lon)), float("{0:.6f}".format(lat + dec_lat))])

    return out


def locs_generator():
    out = []
    for _ in xrange(1000):
        lat = random.randint(-120, -70) # US longitude and latitudes
        lon = random.randint(30, 45)
        numrows = random.randint(1, 20)
        out = out + random_lats_longs(lat, lon, numrows, random_id())

    return out


def chal1():
    rows = make_records()
    rows.append([
        fake.ssn(),
        "Megan Fox",
        fake_address(),
        "Actress",
        fake.phone_number(),
        "Sunburn"
    ])
    readme = """CHALLENGE 1

Quick warmup: why did Megan Fox see the doctor? The name of the condition is the password for the next level.
    """
    write_challenge("chal1", "", rows, readme)


def chal2():
    rows = make_records()

    occs = [rec[3] + rec[5] for rec in rows]
    while most_common(occs) != "LawyerCirrhosis":
        record = [
            fake.ssn(),
            fake.name(),
            fake_address(),
            "Lawyer",
            fake.phone_number(),
            "Cirrhosis"
        ]
        rows.append(record)
        occs = [rec[3] + rec[5] for rec in rows]

    readme = """CHALLENGE 2

Second warmup: which occupation suffers cirrhosis the most?
    """
    write_challenge("chal2", "-pSunburn", rows, readme)


def chal3():
    rows = [[hashlib.md5(field).hexdigest() for field in record]
            for record in make_records()]
    rows.append([
        hashlib.md5(fake.ssn()).hexdigest(),
        hashlib.md5("Mike Pence").hexdigest(),
        hashlib.md5(fake_address()).hexdigest(),
        hashlib.md5("Vice President").hexdigest(),
        hashlib.md5(fake.phone_number()).hexdigest(),
        hashlib.md5("Flatulence").hexdigest()
    ])
    readme = """CHALLENGE 3

Someone thought that hashing made data irrecoverable. Recover Mike Pence's condition. It is the password to the next level.
    """
    write_challenge("chal3", "-pLawyer", rows, readme)


def chal4():
    rows = [[custom_hash(v) if i != 5 else v for i, v in enumerate(record)]
            for record in make_records()]
    rows2 = [[custom_hash(v) if i != 5 else v for i,
              v in enumerate(record)] for record in rows]
    rows2.append([
        custom_hash(fake.ssn()),
        custom_hash(fake.name()),
        custom_hash(fake_address()),
        custom_hash(fake.job()),
        custom_hash(fake.phone_number()),
        "Stillbirth"
    ])
    rows2.append([
        custom_hash(fake.ssn()),
        custom_hash(fake.name()),
        "2f2f9ebae84121d7668a1e91c976b7a7",
        custom_hash(fake.job()),
        custom_hash(fake.phone_number()),
        "Ingrown toenail"
    ])
    rows2.append([
        custom_hash(fake.ssn()),
        custom_hash(fake.name()),
        custom_hash(fake_address()),
        custom_hash(fake.job()),
        custom_hash(fake.phone_number()),
        "Turner Syndrome"
    ])
    rows2.append([
        custom_hash(fake.ssn()),
        custom_hash(fake.name()),
        custom_hash(fake_address()),
        custom_hash(fake.job()),
        custom_hash(fake.phone_number()),
        "Ovarian Cancer"
    ])
    readme = """CHALLENGE 4

The clinic has learned its lesson and realised that it needs to anonymise personally-identifying info more effectively. But it still wants to release data on the conditions it treats. It decides to publish the conditions in the clear, but to re-anonymise all other data using a decent hash fuction each time it is downloaded.

You download a dump of the database one day. 3 hours later, Piers Morgan is seen walking into the clinic. You request another dump of the database ('chal4later.csv'). What condition was he treated for? 

Concatenate to the condition the hash of his address to get the password for the next level, replacing any spaces with underscores i.e. (Brain_Tumour688e5e598349d9bb50e1b69b4c909bf93)
    """
    write_challenge("chal4", "-pFlatulence", rows,
                    readme, "chal4later.csv", rows2)


def chal5():
    ADDRESS = "1460 Claridge Drive, Beverly Hills, CA 90210"
    rows = [[custom_hash(v) if i != 1 else v for i, v in enumerate(record)]
            for record in make_records()]
    rows2 = [["" if (i == 1 or i == 2) and j % 2 == 0 else v for i, v in enumerate(
        record)] for j, record in enumerate(make_movie_records())]
    rows.append([
        custom_hash(fake.ssn()),
        "Jill Abramson",
        custom_hash(ADDRESS),
        custom_hash("Newspaper Editor"),
        custom_hash(fake.phone_number()),
        custom_hash(rand.choice(DISEASES))
    ])
    rows2.append([
        "Jill Abramson",
        "",
        "",
        "Apocalypse Now",
        custom_hash("Apocalypse Now")
    ])

    rows.append([
        custom_hash(fake.ssn()),
        "Cornelia Griggs",
        custom_hash(ADDRESS),
        custom_hash(fake.job()),
        custom_hash(fake.phone_number()),
        custom_hash(rand.choice(DISEASES))
    ])
    rows2.append([
        "Cornelia Griggs",
        ADDRESS,
        custom_hash(ADDRESS),
        "Love Actually",
        custom_hash("Love Actually")
    ])
    ADDRESS7 = "7999 Sanders Lock, Lake Jesseside, WI 43820-9076"
    MOVIE7 = "The Cure For Insomnia"
    rows2.append([
        fake.name(),
        ADDRESS7,
        custom_hash(ADDRESS7),
        MOVIE7,
        custom_hash(MOVIE7)
    ])

    rand.shuffle(rows2)
    rows2.insert(0, MOVIE_COLS)
    with open('chal5movies.txt', 'wb') as of:
        wr = csv.writer(of)
        wr.writerows(rows2)

    readme = """CHALLENGE 5

A list of just names and hashed data has been released. 

Determine Jill Abramson's address. The name of the road plus the zip code in the format "Road_Name_XXXXX" is the next password.

Hint: a nearby movie rental store (with a database system made my the same company that did the clinic's) recently had its database cracked by a rival group of hackers.
    """

    write_challenge(
        "chal5", "-pIngrown_toenail2f2f9ebae84121d7668a1e91c976b7a7", rows, readme)


def chal6():
    rows = make_records()
    rows.append([
        fake.ssn(),
        "David Dreier",
        "3 Santa Cruz Street, Laguna Beach, CA 92651",
        "Politican",
        fake.phone_number(),
        "Toothache"
    ])

    rows2 = locs_generator()

    ID = random_id()
    rows2.append([
        ID,
        33.532699,
        -117.769421
    ])
    rows2.append([
        ID,
        33.531554,
        -117.774201
    ])

    readme = """CHALLENGE 6

It's been a bad week for David Dreier.

First the clinic he went to once to treat his toothache got hacked. Things could have been worse... he thought at the time.

Next an Android game he played got hacked, leaking anonymised location information of all its users. Nobody paid much attention at first because the data was incomplete. But it's potentially career-ending news for David.

The password is the url of the website of a particular building (excluding http:// and www.).
    """

    write_challenge("chal6", "-pClaridge_Drive_90210", rows,
                    readme, "chal6locations.csv", rows2, LOCATION_COLS)


def chal7():
    rows = [[]]
    readme = """CHALLENGE 7

This time, the clinic's database is well-secured and has not been leaked. But one of the patients decided to use their favourite film (no spaces) with their house number appended as the password to the clinic online portal (easy to remember, right?). It is also the password to the next challenge.

Hint: you'll need the movies db you found in challenge 5, there is no medical data in this challenge.

Note: bruteforcing allowed here.
    """

    write_challenge("chal7", "-pmainstreet-bar.com", rows, readme)


def chal8():
    rows = [[]]
    readme = """Wait, there's no challenge here...
    
Congratulations, you completed this mini-CTF. And if you got here first, you won!

    """

    write_challenge("chal8", "-pTheCureForInsomnia7999", rows, readme)


chal1()
chal2()
chal3()
chal4()
chal5()
chal6()
chal7()
chal8()
