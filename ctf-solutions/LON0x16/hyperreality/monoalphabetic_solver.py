#!/usr/bin/python3

from collections import Counter

with open('croatian_monoalphabetic.txt') as f:
    ciphertext = f.read().strip()

print(len(set(ciphertext)))

# replace unicode nonsense with numbers to work with more easily
seen = {}
replaced = []
cur_ascii = 48
for c in ciphertext:
    if c not in seen:
        seen[c] = cur_ascii
        cur_ascii += 1
    replaced.append(seen[c])

# insert spaces
print(Counter(replaced).most_common())
replaced = [' ' if c == 55 else c for c in replaced]

# find longest unbroken run of characters: it's most likely the flag
run = 0
longest_run = 0
end_index = 0
for i, c in enumerate(replaced):
    if c == ' ':
        if run > longest_run:
            end_index = i
            longest_run = run
        run = 0
    else:
        run += 1

flag = replaced[end_index - longest_run:end_index]
print(flag)

replaced = ['f' if c == 97 else c for c in replaced]
replaced = ['l' if c == 67 else c for c in replaced]
replaced = ['a' if c == 51 else c for c in replaced]
replaced = ['g' if c == 58 else c for c in replaced]
replaced = ['{' if c == 124 else c for c in replaced]
replaced = ['}' if c == 127 else c for c in replaced]
replaced = ['_' if c == 126 else c for c in replaced]

# frequency analysis + manual tweaking
# https://www.sttmedia.com/characterfrequency-croatian
replaced = ['i' if c == 64 else c for c in replaced]
replaced = ['e' if c == 60 else c for c in replaced]
replaced = ['o' if c == 57 else c for c in replaced]
replaced = ['n' if c == 56 else c for c in replaced]
replaced = ['r' if c == 49 else c for c in replaced]
replaced = ['t' if c == 52 else c for c in replaced]
replaced = ['j' if c == 65 else c for c in replaced]
replaced = ['s' if c == 53 else c for c in replaced]
replaced = ['u' if c == 69 else c for c in replaced]
replaced = ['k' if c == 54 else c for c in replaced]
replaced = ['v' if c == 50 else c for c in replaced]
replaced = ['y' if c == 125 else c for c in replaced]
replaced = ['d' if c == 66 else c for c in replaced]

flag = replaced[end_index - longest_run:end_index]

print(''.join([str(c) for c in replaced]))
print(Counter(replaced).most_common())
print(''.join([str(c) for c in flag]))
