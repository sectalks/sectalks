#!/usr/bin/env python
 
import sys
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import zlib
 
if len(sys.argv) > 1:
    packets = rdpcap(sys.argv[1])
    res = bytearray()
    for packet in packets:
        res.append(bytes(packet)[23])

    print((zlib.decompress(str(res))).decode())