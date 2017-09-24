## LON0x0d Archive

We are presented with a 7zip archive, containing 16 more 7zip archives named after each of the hexadecimal characters, each of which contain 16 of the same, and so on. 

Since we don't know how deep the rabbit hole goes, it could be dangerous to write a script to recursively decompress everything. This could quickly turn into a self-inflicted ["zip bomb"](https://en.wikipedia.org/wiki/Zip_bomb) of our filesystem. So the next step was to look for a distinguishing feature that might reveal the one true decompression path.

`ls` showed that one of the archives was bigger than the others, so I decompressed it. One of the resulting files was again larger than the others, so I decompressed that. About ten levels down, I found myself wishing I had automated this process, but was in too deep to bother doing that now! 

Eventually I hit the bottom, which consisted of 16 .txt files. However, I opened a few and all said "The answer is not here". Bah.

This made me suspect that I should have been taking note of the hexadecimal names of the zip files that I decompressed. Perhaps these would together form the flag. I deleted the folder and began the painstaking decompression process all over again. The question master seemed rather amused by this, and I didn't know why... yet.

The pressure was on. Two other contestants were only one challenge away from victory. After messing up the decompression half way through and having to start over again, I submitted the complete hexadecimal string to the website, but it wasn't correct! Nooo, now what?

Taking another look at the text files but this time doing `strings *.txt` to see just the text, there was the flag, in plain sight all along! Fortunately I didn't spend too long facepalming before submitting it. Lessons learned:

 - Don't be lazy, script this stuff from the beginning.
 - Read all the files you are given, rather than assuming they all say "the answer is not here"!
 - [Zip-quines are a thing](https://research.swtch.com/zip), if the question master wanted to be even more devilish.

To absolve myself of my laziness, here is a scripted solution:

```bash
#!/bin/bash

# Place in an empty folder with the archive file

7z x archive.7z
mv archive.7z /tmp/

while [ $? -ne 2 ]; do 
    biggest=$(ls -l | awk '{print $5" "$9}' | sort -n -r | head -n 1 | awk '{print $2}')
    7z x $biggest -y
done

strings *.txt
mv /tmp/archive.7z . 
```
