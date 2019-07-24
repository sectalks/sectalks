#!/usr/bin/python3

from collections import Counter
import operator
import re

with open('challenge_files/lolhex.txt') as f:
    text = f.read().strip()

chars = text


evens = [v for i,v in enumerate(chars) if i % 2 == 0]
odds = [v for i,v in enumerate(chars) if i % 2 == 1]

# print(Counter(evens).most_common())
# [('e', 10461), ('7', 4880), ('5', 3580), ('8', 334), ('c', 136), ('a', 50), ('9', 44)]


def swap(froms, to):
    global chars
    chars = chars.replace(froms, 'X')
    chars = chars.replace(to, froms)
    chars = chars.replace('X', to)

swap('e', '6')
swap('5', '2')
swap('8', '0')
swap('9', '5')
swap('9', 'a')
swap('8', 'e')
swap('1', 'f')
swap('f', '9')
swap('c', '4')
swap('f', '3')
swap('d', 'f')
swap('8', 'c')

# print(''.join(chars))

hexes = [i for i in re.findall('.{2}', chars)]
print(''.join([chr(int(i, 16)) for i in hexes]))
print(Counter(hexes).most_common())


# print(evens)
# print(set(evens))
# print(odds)
# print(set(odds))

bla = [i for i in re.findall('.{2}', text)]
print(Counter(bla).most_common())



# a = """Students compile a collection of their texts in a variety of genres over time and choose two pieces to present for summative assessment. In the majority of cases, the work in the student’s collection will arise from normal classwork, as the examples below illustrate. 
 
#  The annotations capture insights by the student’s teacher, using the features of quality, with a view to establishing the level of achievement the text reflects. The purpose of the annotations is to make the teacher's thinking visible. The annotations were confirmed by the Quality Assurance group, consisting of practicing English teachers and representatives of the Inspectorate, the SEC and JCT."""
# print([hex(ord(i)) for i in a])
