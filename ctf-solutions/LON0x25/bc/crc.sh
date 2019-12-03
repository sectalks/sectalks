#!/usr/bin/env bash
echo -e "sign\nadmin=ye" | \
nc mtg.wtf 9000 | \
sed -n '/^Cookie/{s/.*mac":\(.*\)}/\1/p}' | \
python3 -c "
import sys
import zlib
import json
print('login')
print(json.dumps(dict(msg='admin=yes',mac=zlib.crc32(b's', int(sys.stdin.readline().strip())))))
" | \
nc mtg.wtf 9000
