# Hosting a JS Deobfuscation CTF

## Challenge

Reverse engineer the JavaScript code.  Simplify it to the point you can actually understand what's going and figure out how toget the flag.

Recommended tooling:

* Use [Chrome Devtools Local Overrides](https://developers.google.com/web/updates/2018/01/devtools#overrides) to be able to change the scripts.
* Use a code editor that can intelligently rename JavaScript variables, e.g. Visual Studio Code.

## Concepts

The aim of the challenge is to introduce people to some of the following JS language oddities and malware techniques:

* Minification... replace var names, remove comments
* Compression... string, decompress, eval
* Obfuscate... use encodings e.g. escape/unescape, encryption, object vs array notation, multiple script parts, dead code, reusing same variable names
* Anti-emulation... detect debugger, DOM events, elapsed time, emulation limits, exception handling, parent/child pages, 
* Subtle JS equality issues (https://dorey.github.io/JavaScript-Equality-Table/)
* Subtle JS behaviours (https://www.smashingmagazine.com/2011/10/lessons-from-a-review-of-javascript-code/)... uncommon radix, lambdas, self-execution functions

## Run the challenge

The easy challenge introduces JS skills and standard malware obfuscation practices, but doesn't do too much to prevent debugging, logging, or other reversing techniques.

`docker build -t sectalks:easy . && docker run -p 9080:9080 -ti --rm=false -e FLAG="insert_credit_card_here" sectalks:easy`

The hard challenge builds on the same foundation, but adds more code obfuscation and anti-forensics tricks.

`docker build -t sectalks:hard . && docker run -p 9081:9080 -ti --rm=false -e FLAG="skimmer_surcharge_applied" sectalks:hard`