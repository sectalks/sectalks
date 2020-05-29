#!/bin/bash

HOST=sectalks-ctf.caller.xyz

nc -z $HOST 107 110 111
nc -uz $HOST 99
nc -z $HOST 75

nc $HOST 61217
