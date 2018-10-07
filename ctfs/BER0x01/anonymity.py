#!/usr/bin/env/python2

import csv
import os
import random
from faker import Faker
import hashlib
import subprocess
from collections import Counter

fake = Faker()
rand = random.SystemRandom()

with open("diseases.txt") as f:
    DISEASES = [line.strip() for line in f.readlines()]

with open("movies.txt") as f:
    MOVIES = [line.strip() for line in f.readlines()]

COLS = ["SSN", "Name", "Address", "Occupation", "Phone Number", "Condition"]
MOVIE_COLS = ["Name", "Address", "addr_hash", "Rented Movie", "movie_hash"]
LOCATION_COLS = ["user_id", "lat", "long"]

chal1_disease = "Acne"

chal2_job = "Driver"

chal3_disease = "Itching"

chal4_disease = "Loss of libido"
chal4_address_hash = "50194388f8466ff169c35d7a00a92f87"
chal4_password = chal4_disease.replace(" ", "_") + chal4_address_hash

chal5_address = "4300 Brown Street, Walnut Creek, CA 94596"
chal5_password = "Brown_Street_94596"

chal6_website = "smcgov.org"
chal6_coordinates = [[37.455630, -122.439630], [37.456019, -122.444718]]
chal6_address = "915 Railroad Ave, Half Moon Bay, CA 94019, USA"

chal7_movie = "Pirates of the Caribbean"
chal7_address = "2160  Locust Street, Albany GA, 31707"
chal7_password = chal7_movie.replace(" ", "") + "2160"


def write_challenge(
    outfile, password, rows, readme, extra_name="", extra_data="", extra_cols=COLS
):
    csv_name = outfile + ".csv"
    zip_name = outfile + ".zip"
    readme_name = outfile + "README.txt"

    rand.shuffle(rows)
    rows.insert(0, COLS)
    with open(csv_name, "wb") as of:
        wr = csv.writer(of)
        wr.writerows(rows)

    if extra_data:
        rand.shuffle(extra_data)
        extra_data.insert(0, extra_cols)
        with open(extra_name, "wb") as of:
            wr = csv.writer(of)
            wr.writerows(extra_data)

    with open(readme_name, "w") as of:
        of.write(readme)

    print "###################"
    print outfile
    print password
    print "###################"

    subprocess.call(
        ["7z", "a", password, "-y", zip_name, csv_name, readme_name, extra_name]
    )

    # cleanup
    os.remove(csv_name)
    if extra_name:
        os.remove(extra_name)
    os.remove(readme_name)


def fake_address():
    return fake.address().replace("\n", ", ")


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
            rand.choice(DISEASES),
        ]
        rows.append(record)

    return rows


def make_movie_records(size=1000):
    rows = []
    for i in range(size):
        addr = fake_address()
        movie = rand.choice(MOVIES)
        record = [fake.name(), addr, custom_hash(addr), movie, custom_hash(movie)]
        rows.append(record)

    return rows


def most_common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]


def random_id():
    return ("%012x" % random.randrange(16 ** 12)).lower()


def random_lats_longs(lat, lon, num_rows, random_id):
    out = []
    for _ in xrange(num_rows):
        dec_lat = random.random() / 5
        dec_lon = random.random() / 5
        out.append(
            [
                random_id,
                float("{0:.6f}".format(lon + dec_lon)),
                float("{0:.6f}".format(lat + dec_lat)),
            ]
        )

    return out


def locs_generator():
    out = []
    for _ in xrange(1000):
        lat = random.randint(-120, -70)  # US longitude and latitudes
        lon = random.randint(30, 45)
        numrows = random.randint(1, 20)
        out = out + random_lats_longs(lat, lon, numrows, random_id())

    return out


def chal1():
    rows = make_records()
    # add this one to allow the challenge 3 hash to be computed
    rows.append(
        [
            fake.ssn(),
            fake.name(),
            fake_address(),
            fake.job(),
            fake.phone_number(),
            chal3_disease,
        ]
    )
    rows.append(
        [
            fake.ssn(),
            "Megan Fox",
            fake_address(),
            "Actress",
            fake.phone_number(),
            chal1_disease,
        ]
    )
    readme = """CHALLENGE 1

Quick warmup: why did Megan Fox see the doctor? The name of the condition is the password for the next level.
    """
    write_challenge("chal1", "", rows, readme)


def chal2():
    rows = make_records()

    occs = [rec[3] + rec[5] for rec in rows]
    while most_common(occs) != chal2_job + "Cirrhosis":
        record = [
            fake.ssn(),
            fake.name(),
            fake_address(),
            chal2_job,
            fake.phone_number(),
            "Cirrhosis",
        ]
        rows.append(record)
        occs = [rec[3] + rec[5] for rec in rows]

    readme = """CHALLENGE 2

Second warmup: which occupation suffers cirrhosis the most?
    """
    write_challenge("chal2", "-p" + chal1_disease, rows, readme)


def chal3():
    rows = [
        [hashlib.md5(field).hexdigest() for field in record]
        for record in make_records()
    ]
    rows.append(
        [
            hashlib.md5(fake.ssn()).hexdigest(),
            hashlib.md5("Mike Pence").hexdigest(),
            hashlib.md5(fake_address()).hexdigest(),
            hashlib.md5("Vice President").hexdigest(),
            hashlib.md5(fake.phone_number()).hexdigest(),
            hashlib.md5(chal3_disease).hexdigest(),
        ]
    )
    readme = """CHALLENGE 3

Someone thought that hashing made data irrecoverable. Recover Mike Pence's condition. It is the password to the next level.
    """
    write_challenge("chal3", "-p" + chal2_job, rows, readme)


def chal4():
    rows = [
        [custom_hash(v) if i != 5 else v for i, v in enumerate(record)]
        for record in make_records()
    ]
    rows2 = [
        [custom_hash(v) if i != 5 else v for i, v in enumerate(record)]
        for record in rows
    ]
    rows2.append(
        [
            custom_hash(fake.ssn()),
            custom_hash(fake.name()),
            custom_hash(fake_address()),
            custom_hash(fake.job()),
            custom_hash(fake.phone_number()),
            "Stillbirth",
        ]
    )
    rows2.append(
        [
            custom_hash(fake.ssn()),
            custom_hash(fake.name()),
            chal4_address_hash,
            custom_hash(fake.job()),
            custom_hash(fake.phone_number()),
            chal4_disease,
        ]
    )
    rows2.append(
        [
            custom_hash(fake.ssn()),
            custom_hash(fake.name()),
            custom_hash(fake_address()),
            custom_hash(fake.job()),
            custom_hash(fake.phone_number()),
            "Turner Syndrome",
        ]
    )
    rows2.append(
        [
            custom_hash(fake.ssn()),
            custom_hash(fake.name()),
            custom_hash(fake_address()),
            custom_hash(fake.job()),
            custom_hash(fake.phone_number()),
            "Ovarian Cancer",
        ]
    )
    readme = """CHALLENGE 4

The clinic has learned its lesson and realised that it needs to anonymise personally-identifying info more effectively. But it still wants to release data on the conditions it treats. It decides to publish the conditions in the clear, but to re-anonymise all other data using a decent hash fuction each time it is downloaded.

You download a dump of the database one day. 3 hours later, Piers Morgan is seen walking into the clinic. You request another dump of the database ('chal4later.csv'). What condition was he treated for? 

Concatenate to the condition the hash of his address to get the password for the next level, replacing any spaces with underscores i.e. (Brain_Tumour688e5e598349d9bb50e1b69b4c909bf93)
    """
    write_challenge(
        "chal4", "-p" + chal3_disease, rows, readme, "chal4later.csv", rows2
    )


def chal5():
    rows = [
        [custom_hash(v) if i != 1 else v for i, v in enumerate(record)]
        for record in make_records()
    ]
    rows2 = [
        ["" if (i == 1 or i == 2) and j % 2 == 0 else v for i, v in enumerate(record)]
        for j, record in enumerate(make_movie_records())
    ]
    rows.append(
        [
            custom_hash(fake.ssn()),
            "Jill Abramson",
            custom_hash(chal5_address),
            custom_hash("Newspaper Editor"),
            custom_hash(fake.phone_number()),
            custom_hash(rand.choice(DISEASES)),
        ]
    )
    rows2.append(
        ["Jill Abramson", "", "", "Apocalypse Now", custom_hash("Apocalypse Now")]
    )

    rows.append(
        [
            custom_hash(fake.ssn()),
            "Cornelia Griggs",
            custom_hash(chal5_address),
            custom_hash(fake.job()),
            custom_hash(fake.phone_number()),
            custom_hash(rand.choice(DISEASES)),
        ]
    )
    rows2.append(
        [
            "Cornelia Griggs",
            chal5_address,
            custom_hash(chal5_address),
            "Love Actually",
            custom_hash("Love Actually"),
        ]
    )

    # Data for the last challenge
    rows2.append(
        [fake.name(), chal7_address, custom_hash(chal7_address), chal7_movie, custom_hash(chal7_movie)]
    )

    rand.shuffle(rows2)
    rows2.insert(0, MOVIE_COLS)

    readme = """CHALLENGE 5

A list of just names and hashed data has been released. 

Determine Jill Abramson's address. The name of the road plus the zip code in the format "Road_Name_XXXXX" is the next password.

Hint: a nearby movie rental store (with a database system made my the same company that did the clinic's) recently had its database cracked by a rival group of hackers.
    """

    write_challenge(
        "chal5", "-p" + chal4_password, rows, readme, "chal5movies.csv", rows2
    )


def chal6():
    rows = make_records()
    rows.append(
        [
            fake.ssn(),
            "David Dreier",
            chal6_address,
            "Politican",
            fake.phone_number(),
            "Toothache",
        ]
    )

    rows2 = locs_generator()

    ID = random_id()
    rows2.append([ID, chal6_coordinates[0][0], chal6_coordinates[0][1]])
    rows2.append([ID, chal6_coordinates[1][0], chal6_coordinates[1][1]])

    readme = """CHALLENGE 6

It's been a bad week for David Dreier.

First the clinic he went to once to treat his toothache got hacked. Things could have been worse... he thought at the time.

Next an Android game he played got hacked, leaking anonymised location information of all its users. Nobody paid much attention at first because the data was incomplete. But it's potentially career-ending news for David.

The password is the url of the website of a particular building (excluding http:// and www.).
    """

    write_challenge(
        "chal6",
        "-p" + chal5_password,
        rows,
        readme,
        "chal6locations.csv",
        rows2,
        LOCATION_COLS,
    )


def chal7():
    rows = [[]]
    readme = """CHALLENGE 7

This time, the clinic's database is well-secured and has not been leaked. But one of the patients decided to use their favourite film (no spaces) with their house number appended as the password to the clinic online portal (easy to remember, right?). It is also the password to the next challenge.

Hint: you'll need the movies db you found in challenge 5, there is no medical data in this challenge.

Note: bruteforcing allowed here.
    """

    write_challenge("chal7", "-p" + chal6_website, rows, readme)


def chal8():
    rows = [[]]
    readme = """Wait, there's no challenge here...
    
Congratulations, you completed this mini-CTF. And if you got here first, you won!

    """

    write_challenge("chal8", "-p"+chal7_password, rows, readme)


chal1()
chal2()
chal3()
chal4()
chal5()
chal6()
chal7()
chal8()
