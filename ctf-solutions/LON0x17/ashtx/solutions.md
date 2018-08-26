# London SecTalk 0x17 Solutions

## Agent Secure System v1

I actually solved this one after v2 and v3, as I was working with a friend during the challenge and he solved this one. So it turns out after v2 and v3 this one was easy. 

The program required a username argument like v2. So I ran it and it printed a security error message, as I expected.

`It appears you are attemtping to use Agent Smith's Secure System 1.0 validator.
This violation will be reported to the GGoCySEA Information Security Team.
Please review your security procedures and use the correct Secure System 1.0
Validator that has been issued to you`

So to see what system calls it was making I ran it with strace, but nothing interesting. So I moved on to seeing what library calls it was making by running it through ltrace, this turned up something interesting. Like v2 it was comparing a string, but this time it looks like it was comparing the username string I provided to "agent.smith".

So I simply changed the username argument to ***agent.smith*** and it gave me the token.

`Hello Agent Smith, welcome to the Agent Secure System 1.0 Validator. 
th3 us3r t0k3n y0u s33k is: [hidden]`

## Agent Secure System v2

This was an interesting one to solve. The binary we were given gave the appearence of providing a token if the system is considered to be secure. The binary required a single parameter, supposedly the username.

`The file was a 64-Bit ELF file, built for Linux 3.2. So the next logical step was to run it through`

Running the program with the username parameter it indicated the system was not secure, so could not run. The next logical step was to run it through strace to see what system calls were being made, maybe it was looking for a particular file?

It wasn't trying to read any files, other than the libraries it required.

```
  linux-vdso.so.1 (0x00007ffcd83ea000)
  libc.so.6 => /usr/lib/libc.so.6 (0x00007f5e89e25000)
  /lib64/ld-linux-x86-64.so.2 => /usr/lib64/ld-linux-x86-64.so.2 (0x00007f5e8a01e000)
```

So to see what calls it was making to the libraries I ran it through ltrace. This returned something more promising, as it was making calls to set an environment variable ***agent_term_secure***.

```
 setenv("agent_term_secure", "ass-is-not-secure", 1) 
```

It was then pulling this env variable and comparing it to "secureseedvalueplacement"

```
 getenv("agent_term_secure") = "ass-is-not-secure"
 strcmp("ass-is-not-secure", "secureseedvalueplacement")
```

So if I could change ***agent_term_secure*** to match the compared value, it may give us the token/flag we are looking for. This wasn't as simple as setting the environmental variable, as this would be overwritten when the function was called within the program.

So the next step I took was dissasembling the binary with objdump to see if the token/flag we were looking for could be easily extracted from the code. This wasn't so easy as it appears to be built logically, and while reverse engineering it is possible, it would take a significant amount of time. 

So instead I opted to go down the route of trying to hack the binary into revealing the code. So I stepped through the program with the GNU debugger. Breaking at the setenv function. As I stepped through I reached a critical logic point, where the strcmp on the environmental variable is done.

```
0x5555555558ba  call   0x555555555030 <getenv@plt>                                                                                                                                                              
0x5555555558e2  lea    rdx,[rbp-0x3c]                                                                                                                                                                           
0x5555555558e6  mov    rax,QWORD PTR [rbp-0x8]                                                                                                                                                                  
0x5555555558ea  mov    rsi,rdx                                                                                                                                                                                  
0x5555555558ed  mov    rdi,rax                                                                                                                                                                                  
0x5555555558f0  call   0x555555555080 <strcmp@plt>                                                                                                                                                              
0x5555555558f5  test   eax,eax                                                                                                                                                                                  
0x5555555558f7  jne    0x555555555940              
```

Stopping at the jne instruction and printing eflags showed that the Zero Flag bit was not set, so the code will jump away.

```
eflags         0x246    [ PF IF ]
```

So I had to toggle the ZF flag before proceeding.

```
set $eflag ^= (1 << 6)
```

This new cpde path got me a different message.

     `Agent ashtx, it appears you are attemtping to use Agent Smith's Secure System 2.0 validator.
     This violation will be reported to the GGoCySEA Information Security Team.
     Please review your security procedures and use the correct Secure System 2.0 application that has been issued to you`
     
It seems I had hit another jump point where it was comparing the username, so I did the same as I did above and flipped the result. Then voila!

     `Hello Agent Smith, welcome to the Agent Secure System 2.0 Validator. th3 syst3m t0k3n y0u s33k is: [hidden]`

## Agent Secure System v3

This one was tricky, as I had followed the flow and gone down all the logical routes of the main code and ended up with either errors or success. So I decided to dig through the code and luckily hit upon an unreferenced code which was printing something at ***0x11a5***.

So I loaded up gdb again, breaking at the same point I did in v2, but this time I adjusted the Program Counter to execute the section I had found at ***0x11a5***. Success! It printed the token.

aaa th3
fff 3331337
bbb t0k3n
ccc y0u
ddd s33k
eee is:
yyy [hidden]

## Bacon v1

This was a tough one, and I approached it in the completly wrong way. But not surpising as I haven't touched crypto algorithms since University. But to cut a long story short I tried various methods to try and identify the cipher, which happened to be staring me in the face the entire time, as it was in the challenge name. Thanks to hyperreality for the hint. Bacon cipher must be in the same naming bucket as Cocktail sort.

A quick Wikipedia search gave me everything I needed to know about the keyless cipher. So I just had to decode the message by grouping the 0's and 1's from the upper-case and lower-case characters respectively, and success, I decrypted the message.

## Bacon v2

Given my success with v1, I was more confident about v2. Luckily I had already read the details about the first and second version of the Bacon algorithm. So when presented with the message, it was clear the fonts used per character were different. This was how you identify the ciphertext, one font represents 0 the other font respresents 1.

The file was identified as UTF-8 encoded, and running it through xxd showed that some bytes were US-ASCII encoded, and others were not. The ones not decoded as US-ASCII characters were clearly the Unicode characters.

So using the browser rendered text and the bytes I identified as US-ASCII. I was able to decode the message. This was after the spaces had been removed.

This was a very manual approach, but as I didn't have a good working knowledge of UTF-8 encoding at the time, I decided it was the quickest.

## Dodgy Drive

This one was tricky as my I have little to no experience reverse engineering binaries, and from trying to detect the file type, it had identified it as an Applesoft BASIC program data file

```
 inject.bin: Applesoft BASIC program data, first line number 8
```

So I started looking for methods of decompiling the binary. However this turned out to be futile, but not all hope was lost as a hint was given to solving the challenge, which I feel like I should have slapped myself for not thinking of earlier. Googling the file name ***inject.bin*** immediately returned dozens of results for USB Rubber Ducky related content.

The USB Rubber ducky is a keystroke injection tool disguised as a generic USB flash drive but actually presents itself as a USB HID Keyboard to the host when plugged in, and inject.bin is the payload to be dropped, compiled from Ducky Script.

So now I knew what it was, I just needed a way to decompile it or failing that run it. The former was the easier option, so after a little digging I was able to find a decoder written by [hak5darren on github](https://github.com/hak5darren/USB-Rubber-Ducky). 

Running it through the decoder, I was presented with more or less the original Ducky Code which included the flag. Success!


## Nothing in here

I approached this one with caution as I was expecting a tar bomb. So I used tar to list the contents rather than extracting.

```
 tar -tvf nothing_in_here.tar
```

As described in the challenge, the directory structure was deep, however the noise was from nested folders with the same name, "nothing in here", which most ended up being dead ends. So to cut down the noise I excluded paths ending in that directory name.

```
 tar -tvf nothing_in_here.tar | grep -v 'nothing in here/$'
```

To my luck this immediately printed the flag as well as a few other dead ends such as "jk lol" and "something in here". 

```
 ../nothing in here/f l a g { t h i n k _ o f _ t h e _ i n o d e s }/
```

I had found what I was looking for and just had to remove the spaces

```
 echo "f l a g { t h i n k _ o f _ t h e _ i n o d e s }" | tr -d '[:space:]'
```
