"""
Requires `7za` to be installed on your machine and the additional data leak to be in a file named
leaked_rented_movie_customers.txt.

Can probably reduce the brute-forcing needed by eliminating those without addresses.

Took nearly 2 minutes to complete on my laptop.

> python3 chal7.py
...
...
...
--------------------------------------------------------------------------------
[583 / 1003] trying password Dekalog81809

7-Zip (a) [64] 16.02 : Copyright (c) 1999-2016 Igor Pavlov : 2016-05-21
p7zip Version 16.02

Scanning the drive for archives:
1 file, 368 bytes (1 KiB)

Extracting archive: chal8.7z
--
Path = chal8.7z
Type = 7z
Physical Size = 368
Headers Size = 192
Method = LZMA2:12 7zAES
Solid = +
Blocks = 1


Would you like to replace the existing file:
  Path:     ./chal8.csv
  Size:     59 bytes (1 KiB)
  Modified: 2019-08-22 18:31:41
with the file from archive:
  Path:     chal8.csv
  Size:     59 bytes (1 KiB)
  Modified: 2019-08-22 18:31:41
? (Y)es / (N)o / (A)lways / (S)kip all / A(u)to rename all / (Q)uit? A

Everything is Ok

Files: 2
Size:       186
Compressed: 368

password is Dekalog81809

Answer -

Dekalog81809
"""

import csv
import subprocess


with open('leaked_rented_movie_customers.txt') as f:
    leak = list(csv.DictReader(f))

for i, d in enumerate(leak, 1):
    movie_mangled = d['Movie'].replace(' ', '')
    address_bits = d['Address'].split(' ')
    password = f'{movie_mangled}{address_bits[0]}'

    print('-' * 80)
    print(f"[{i} / {len(leak)}] trying password {password}")
    exit_code = subprocess.call(['7za', 'e', '-aoa', f'-p{password}', 'chal8.7z'])
    if exit_code == 0:
        print(f"\npassword is {password}")
        break
