#!/bin/bash

set -euo pipefail

unzip a_little_tricker.jpg &>/dev/null || true
grep STL ' '
rm ' '