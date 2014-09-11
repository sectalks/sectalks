#!/bin/bash
# 
# Bit of a hack so we can run avconv in a while true; do loop, to provide a
# source of streaming audio for Flag #4
avconv -re -c mp3 -i test.mp3 -c pcm_mulaw -ar 8000 -ac 1 -f mulaw udp://localhost:55555
