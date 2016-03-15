
Find a way to print the "win" message.

Category: Reverse engineering

Points: 400

Author: CreateRemoteThread (Norm)

# Rules

* No patching the binary on-disk or in-memory (you can do this, the binary is not obfuscated on purpose).

* There is no "flag" - the point is to get to the "win" message and tell everyone how you did it.

* There's many ways to skin a cat - the most obvious solution may not be the easiest.

# Hints

* Write a python parser (pwntools)

* There's an intentional buffer overflow (i.e. set a value on the stack to X).
