#!/bin/bash

cd /ctf/app/

python server.py
P1=$!

wait $P1