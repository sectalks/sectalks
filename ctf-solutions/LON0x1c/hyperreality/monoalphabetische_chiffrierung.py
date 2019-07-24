#!/usr/bin/python3

from collections import Counter
import operator

with open('challenge_files/monoalphabetische_chiffrierung.txt') as f:
    ciphertext = f.read().strip().lower()

print(len(set(ciphertext)))

def replace(num, to):
    return [to if c == num else c for c in replaced]

# replace unicode nonsense with numbers to work with more easily
seen = {}
replaced = []
cur_ascii = 48
for c in ciphertext:
    if ord(c) >= 120793 and ord(c) <= 120801: # numbers we don't want
        pass
    if c not in seen:
        seen[c] = cur_ascii
        cur_ascii += 1
    replaced.append(seen[c])

print(Counter(replaced).most_common())

# https://www.sttmedia.com/characterfrequency-german
# http://www.languagedaily.com/learn-german/vocabulary/common-german-words
replaced = replace(51, ' ')
replaced = replace(49, 'e')
replaced = replace(56, 'n')
replaced = replace(62, 'i')
replaced = replace(50, 'r')
replaced = replace(53, 'd')
replaced = replace(65, 'u')
replaced = replace(48, 'w')
replaced = replace(61, 't')
replaced = replace(63, 'o')
replaced = replace(73, 'b')
replaced = replace(66, 's')
replaced = replace(55, 'a')
replaced = replace(57, 'c')
replaced = replace(67, 'h')
replaced = replace(52, 'a')
replaced = replace(54, 'v')
replaced = replace(58, 'e')
replaced = replace(59, 'y')
replaced = replace(60, 'p')
replaced = replace(64, 's')
replaced = replace(68, 'w')
replaced = replace(69, 'f')
replaced = replace(70, 'l')


# divide up with spaces and print most common words
counts = {}
cur = []
for c in replaced:
    if c == ' ':
        string = ''.join(str(a) for a in cur)
        if string not in counts:
            counts[string] = 1
        else:
            counts[string] += 1
        cur = []
    else:
        cur.append(c)

sorted_counts = sorted(counts.items(), key=operator.itemgetter(1))

for line, count in sorted_counts:
    print("%7d %s" % (count, line))

for line, count in sorted_counts:
    if 'flag' in line:
        print(line)

print(Counter(replaced).most_common())
print(''.join(map(str, replaced)))
