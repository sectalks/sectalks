#!/usr/bin/env python

import sys
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

def caesar(plaintext, shift):
    result = ''
    for l in plaintext:
        if not l.isalpha():
            result+=l
        else:
            integerValue = ord(l.lower())
            integerValue -= 97
            integerValue += shift
            integerValue %= 26
            integerValue += 97
            if l.isupper():
                result += chr(integerValue).upper()
            else:
                result += chr(integerValue)
    return result

packets = []

flag = 'STL{reproduce_scandalous_gate}'

sport = 1025
time = 1537747200

for c in flag:
    pkt = (Ether(src='de:ad:be:ef:00:00', dst='11:22:33:44:55')/
            IP(src='10.100.100.15', dst='10.100.100.1')/
            UDP(sport=sport,dport=69)/
            caesar(c, 13))
    pkt.time = time
    packets.append(pkt)
    sport += 1
    time += 1

wrpcap('pcap1.pcap', packets)