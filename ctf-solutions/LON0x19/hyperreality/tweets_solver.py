#!/usr/bin/python3

from collections import Counter
import operator

with open('all_tweets.txt') as f:
    ciphertext = f.read().strip()

# print(len(set(ciphertext)))

def replace(num, to):
    return [to if c == num else c for c in replaced]

# replace unicode nonsense with numbers to work with more easily
seen = {}
replaced = []
cur_ascii = 48
for c in ciphertext:
    if c not in seen:
        seen[c] = cur_ascii
        cur_ascii += 1
    replaced.append(seen[c])

print(Counter(replaced).most_common())

# https://en.wikipedia.org/wiki/Most_common_words_in_English
replaced = replace(59, ' ')
replaced = replace(55, 'e')
replaced = replace(63, 't')
replaced = replace(51, 'a')
replaced = replace(69, 'o')
replaced = replace(76, 'n')
replaced = replace(62, 'h')
replaced = replace(88, 'd')
replaced = replace(50, 'b')
replaced = replace(81, 'f')
replaced = replace(54, 'r')
replaced = replace(85, 'D')
replaced = replace(82, '@')
replaced = replace(58, 'l')
replaced = replace(91, 'T')
replaced = replace(54, 'r')
replaced = replace(79, 'u')
replaced = replace(52, 'm')
replaced = replace(64, 'p')
replaced = replace(61, 'y')
replaced = replace(86, 'w')
replaced = replace(57, 'i')
replaced = replace(70, 'g')
replaced = replace(65, 's')
replaced = replace(60, 'H')
replaced = replace(98, 'm')
replaced = replace(87, 'v')
replaced = replace(100, 'A')
replaced = replace(53, 'c')
replaced = replace(80, 'k')
replaced = replace(87, 'v')
replaced = replace(92, 'C')

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

