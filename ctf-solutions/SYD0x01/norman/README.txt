http://advancedpersistentjest.com/2014/11/18/sectalks-2-solution-writeup/

Content copied from the above URL:

Upon unzipping the challenge zip file, we’re met with a complete mess – 200 zip files, and  a picture:

[PICTURE!]

f you try to open some of these zip files, you’ll quickly realize that not all of these files are zips – infact, there’s only one. A quick “file * | grep archive” can show you which file is an actual zip file:

zipfiles

This zipfile is password protected, and the password is “trees” (the MD5 checksum of which is the hash in the image above).

This leads us to the first of two “flags” in the challenge, and two binaries (one for Linux, one for Windows – both 64 bit, unfortunately, due to my extreme laziness). You can find the source code here.

In a nutshell, every time you run the challenge, it allows the user to enter a password of 6 characters in length, 3 times, and compares it against a pre-generated secret key:

challenge-response

If the user is right, a “win” condition is activated, printing the flag. If the user is wrong, it displays an encoded version of the user’s input, and a secret key, encoded in the same manner. The user input and secret key are encoded thusly:

pseudocode

The "win" condition is slightly obfuscated – it’s actually a function, which xor’s each character of the word “PIGEONS” with a static value, to create the value AFLAG42 – the only point to this was to prevent people from running “strings” and calling it a day. The binary itself wasn’t otherwise protected from reverse engineering at all.

The idea is to solve this through either logical deduction, based on the application’s challenge response mechanism, or through IDA pro, which one group managed to do.

All in all, this turned out to be a fairly successful challenge (from an organiser’s perspective), with people solving the challenge in roughly one hour. One area where I could have improved is to protect the original challenge zip file with a password, so everyone had to start at the same time (when I shared the challenge password). Onwards and upwards!
