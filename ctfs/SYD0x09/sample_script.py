#!/usr/bin/python

# to create program socket
# socat tcp-listen:4446,fork exec:./random
# if you don't have socat...get it
# otherwise 
# nc -lvp 4446 -e ./random
# will also work

from socket import *
from time import sleep
import telnetlib, struct

#open up socket. Obviously change port to what you would use
s=socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 4446))

# wait before continuing, allows attaching with gdb.
# probably don't need this.
#raw_input()

# recieve 1024 from socket
data = s.recv(1024)

# print what you have recieved
print data

# send data to socket. Just like interacting with stdin
# don't forget new line for enter
s.send("test string\n")

# solution would like something like

while(1):
  # may need a sleep so buffer doesn't mess up
  # sleep(0.1)
  data = s.recv(1024):
    for 'something' in data:
      # do something, eg send what pokemon you want to play
      s.send("pokemon\n")


# close socket
s.close()
