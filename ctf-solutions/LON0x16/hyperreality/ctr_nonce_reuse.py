#!/usr/bin/python3

# Challenge is similar to https://cryptopals.com/sets/3/challenges/19
# However since we have an idea about the plaintext, we can just:
# - Pick a random tweet
# - Find its matching ciphertext by XORing to get a candidate keystream,
# until we find a keystream that works on another tweet
# - Decrypt all the things

import os
import string

TWEET_PATH = 'encrypted/'

tweet = "Where are the #%*> aliens? https://t.co/FDuJIdwgrN"
print(len(tweet))

# Get shortlist of candidate ciphertexts:
# wc -c * | grep '^.*50 ' | awk '{print $2}' > shortlist
with open('shortlist') as f:
    files = [a.strip() for a in f.readlines()]

for f in files:
    with open(TWEET_PATH + f, encoding="ISO-8859-1") as attempt:
        print(f + ': ', '')
        keystream = [ord(a) ^ ord(b) for a, b in zip(tweet, attempt.read())]

        with open(TWEET_PATH + '0001', encoding="ISO-8859-1") as one:
            out = [a ^ ord(b) for a, b in zip(keystream, one.read())]
            # print(''.join([chr(a) for a in out]))
            if all([c < 128 and chr(c) in string.printable for c in out]):
                break

for f in os.listdir(TWEET_PATH):
    with open(TWEET_PATH + f, encoding="ISO-8859-1") as attempt:
        out = ''.join([chr(a ^ ord(b))
                       for a, b in zip(keystream, attempt.read())])
        if 'flag' in out:
            print(out)
