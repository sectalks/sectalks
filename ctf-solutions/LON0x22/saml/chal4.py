"""
Requires `7za` to be installed on your machine.

Isolates the conditions that either do not exist in chal4.csv or have a different number of rows in chal4later.csv
(16 rows), then 'brute-forces' them by trying them on chal5.7z.

Apparently this isn't brute-forcing because 16 rows is few enough that you could do it by hand :)

> python3 chal4.py
...
...
...
--------------------------------------------------------------------------------
[13 / 16] trying password Ingrown_toenail2f2f9ebae84121d7668a1e91c976b7a7

7-Zip (a) [64] 16.02 : Copyright (c) 1999-2016 Igor Pavlov : 2016-05-21
p7zip Version 16.02

Scanning the drive for archives:
1 file, 276334 bytes (270 KiB)

Extracting archive: ../chal5.7z
--
Path = ../chal5.7z
Type = 7z
Physical Size = 276334
Headers Size = 206
Method = LZMA2:768k 7zAES
Solid = +
Blocks = 1

Everything is Ok

Files: 2
Size:       739320
Compressed: 276334

password is Ingrown_toenail2f2f9ebae84121d7668a1e91c976b7a7

Answer -

Ingrown_toenail2f2f9ebae84121d7668a1e91c976b7a7
"""

from collections import Counter
import csv
import subprocess


with open('chal4.csv') as f:
    data = list(csv.DictReader(f))

with open('chal4later.csv') as f:
    data_later = list(csv.DictReader(f))

conditions_count_in_data = Counter((d['Condition'] for d in data))
conditions_count_in_data_later = Counter((d['Condition'] for d in data_later))

conditions_with_changed_counts = conditions_count_in_data_later - conditions_count_in_data
print(conditions_with_changed_counts)

# dropped Ovarian Cancer, as Piers Morgan is male
conditions_with_changed_counts.pop('Ovarian Cancer')
# dropped Stillbirth, as Piers Morgan is not a baby
conditions_with_changed_counts.pop('Stillbirth')
print(conditions_with_changed_counts)

# 'brute-force' the solution by trying all rows with the conditions with changed counts
matching_data_in_data_later = [d for d in data_later if d['Condition'] in conditions_with_changed_counts]
for i, d in enumerate(matching_data_in_data_later, 1):
    condition_mangled = d['Condition'].replace(' ', '_')
    address_hash = d['Home Address']
    password = condition_mangled + address_hash

    print('-' * 80)
    print(f"[{i} / {len(matching_data_in_data_later)}] trying password {password}")
    exit_code = subprocess.call(['7za', 'e', f'-p{password}', 'chal5.7z'])
    if exit_code == 0:
        print(f"\npassword is {password}")
        break
