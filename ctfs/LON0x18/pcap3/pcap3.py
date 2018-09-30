#!/usr/bin/env python

import sys
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import zlib
import random

packets = []

flag = 'STL{fortunate_abrasive_zoo}'
zflag = zlib.compress(flag)

time = 1537747200

for b in zflag:
    src = '%d.%d.%d.%d' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    pkt = (Ether(src='de:ad:be:ef:00:00', dst='11:22:33:44:55')/
            IP(src=src, dst='10.69.69.1', proto=ord(b), ttl=0)/
            'This is the song that never ends, yes it goes on and on my friend. Some people started singing it, not knowing what it was, and they\'ll continue singing it forever just because...')
    pkt.time = time
    packets.append(pkt)
    time += 1

wrpcap('pcap3.pcap', packets)