#!/bin/bash

set -euo pipefail

echo -n 'STL{TimeCrushBeserkTough}' > ' '
ditto -c -k --sequesterRsrc ' ' flag.zip 
cat a_little_tricker-orig.jpg flag.zip > a_little_tricker.jpg
rm ' ' flag.zip