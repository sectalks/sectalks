#!/bin/bash

# install libfaketime

LD_PRELOAD=/usr/lib/x86_64-linux-gnu/faketime/libfaketime.so.1 \
    FAKETIME="+365d" \
    ./challenge_files/from_future_import_flag_linux
