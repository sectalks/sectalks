# socat -T30 -d -d TCP-LISTEN:6000,fork,reuseaddr EXEC:"python3 -u cerberus.py",pty,echo=0
import sys
import secrets
import uuid
import hashlib
import string
from itertools import islice

loop_count = 5
tag = uuid.uuid4()

flag = 'STL{amazing_homeless_toothbrush}'

def random_chars(size, chars=string.ascii_letters):
    selection = iter(lambda: secrets.choice(chars), object())
    while True:
        yield ''.join(islice(selection, size))

def main():
    print('I needs some proofs of work.')
    random_starts = random_chars(10)
    random_ends = random_chars(6, '0123456789abcdef')

    for i in range(loop_count):
        startswith = next(random_starts)
        l = 15
        endswith = next(random_ends)
        
        sys.stderr.write('{} sending startswith:{}, len:{}, endswith:{} ({}/{})\n'.format(tag, startswith, l, endswith, i+1, loop_count))
        print('Give me a string starting with {}, of length {}, such that its sha1 sum ends in {}.'.format(startswith, l, endswith))

        s = sys.stdin.readline().rstrip()
        sys.stderr.write('{} received {} ({}/{})\n'.format(tag, s, i+1, loop_count))

        if len(s) == l and hashlib.sha1(s.encode()).hexdigest().endswith(endswith):
            print('boom!')
        else:
            print('bzzzzt')
            break
    else:
        sys.stderr.write('{} sending flag!\n'.format(tag))
        print(flag)
    
if __name__ == "__main__":
    main()