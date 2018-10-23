#!/usr/bin/env python
 
import sys
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from httplib import HTTPMessage
import StringIO
import gzip
import re
 
if len(sys.argv) > 1:
     packets = rdpcap(sys.argv[1])
     for packet in packets:
         if packet[TCP].sport == 1337:
             data = packet[TCP].payload
             if len(data) > 0:
                 f = StringIO.StringIO(bytes(data))
                 status_line = f.readline()
                 msg = HTTPMessage(f, 0)
                 body = msg.fp.read()
                 body_stream = StringIO.StringIO(body[4:-7])
                 gzipper = gzip.GzipFile(fileobj=body_stream)
                 data = gzipper.read()
                 m = re.search(r'STL{.*?}', data)
                 if m:
                     print m.group(0)