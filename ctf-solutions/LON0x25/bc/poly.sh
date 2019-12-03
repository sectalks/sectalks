#!/usr/bin/env bash
(echo -e "sign\nbdmin=yes" | nc mtg.wtf 9002; \
 echo -e "sign\ncdmin=yes" | nc mtg.wtf 9002; \
 echo -e "sign\nddmin=yes" | nc mtg.wtf 9002;) | \
sed -n '/^Cookie/{s/^Cookie: \(.*\)/\1/p}' | \
python3 -c "
import json
import sys

cookies = [
    json.loads(sys.stdin.readline().strip())
    for _ in range(3)
]
nonce = cookies[0]['nonce']

if all(c['nonce'] == nonce for c in cookies[1:]):
    derivatives = [b['mac'] - a['mac'] for a, b in zip(cookies, cookies[1:])]
    diff = derivatives[0]
    if all(d == diff for d in derivatives[1:]):
        res = json.dumps(dict(msg='admin=yes', nonce=nonce, mac=cookies[0]['mac'] - diff))
        print('login\n' + res)
    else:
        print('Oops, we hit a modulo boundary.')
else:
    print('Nonces different, try to be faster')
" | \
nc mtg.wtf 9002 | tail -n +5 | head -n -1
