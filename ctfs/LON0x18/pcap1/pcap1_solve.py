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

if len(sys.argv) > 1:
    packets = rdpcap(sys.argv[1])
    flag = ''
    for packet in packets:
        if packet[UDP].dport == 69:
            data = packet[UDP].payload
            if len(data) > 0:
                flag += caesar(bytes(data).decode().rstrip(), 13)
    print flag