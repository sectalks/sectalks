#!/bin/bash

cat <<EOF > crystal_temp.py
import sys

out = ['f'] + [''] * 50

for line in sys.stdin:
    try:
        pos = int(line.strip().split(',')[0], 16)
        hx = int(line.strip().split(',')[1], 16)

        out[pos] = chr(hx)
    except:
        pass

print(''.join(out))
EOF

# Find the verify_password function and grab the relevant disassembled part of it
# Need only the mov and cmp instructions
# Get those on the same line so we have the indices of the flag chars with the chars (both in hex)
# Remove unwanted characters
# Use a quick Python script to parse the hex and rearrange to the flag string

objdump -D challenge_files/crystal_password_validator_linux \
    | grep '43fc69:' -A 570 \
    | egrep 'esi|cmp' \
    | sed '$!N;s/\n/ /' \
    | awk '{print $8 $14}' \
    | sed -e 's/%esi//' -e 's/,%eax//' -e 's/\$//g' \
    | python crystal_temp.py


rm crystal_temp.py
