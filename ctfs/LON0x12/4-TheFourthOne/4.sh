#!/bin/bash

set -euo pipefail

stegano-lsb hide -i errr-orig.png -m "STL{UnknownInnateCombLopsided}" -o errr.png