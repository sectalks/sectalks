#!/bin/bash

# Place in an empty folder with the archive file

# If you extract these in the terminal with 7z you will notice a warning that there is extra data after the end of the archive. Although all the archives appear the same, the extra data at the end differs for the archive files which lead to the solution. cmp, diff or md5sum are all tools that can identify this correct file.

7z x archive.7z -y
mv archive.7z /tmp/

while [ ! -f 0.txt ]; do
    uniqhash=$(md5sum *.7z | awk '{print $1}' | sort | uniq -c | sort -n | head -n1 | awk '{print $2}')

    for file in *.7z; do
        md5=$(md5sum $file | awk '{print $1}')
        if [ $md5 = $uniqhash ]; then
            7z x $file -y
        fi
    done
done

strings *.txt
mv /tmp/archive.7z .
