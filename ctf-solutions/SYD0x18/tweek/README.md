# AV Notes

* main()
   * Read input from user
   * First transformation
* verify_prog()
   * Set up sig handler in case of segfault
   * Second transformation buf -> hash_bytes
* ciaVerified()
   * Popen on “./ciaMalware.sh “ + str + “./flag.txt”

Command injection possible, need to bypass both transformations.

## Command injected

* compiled and executed locally.
* Use the semi-colon to separate command.
* Stdout is read by the calling program and used to decide if malware or not. 
  Not important.
* Had a malformed command trying to execute the output of a command $()
* Turns out stderr is the same as parent process, we can reuse that and read 
  the result out of stderr.
* Can comment out the rest of the command with #

## Second transformation
Simple XOR between two half of the string. That is we need to find X and Y 
such as X^Y is our expected character.

## First transformation
* No transformation when alpha numeric or null-byte
* Otherwise similar to tuple write (where, what)
* Limited to a char that is the first 255 bytes of the buffer.

## Exploitation using pwntools
* Have our command ready:  ; $(head flags.txt) #
* For each character, find a character that when xor is alphanumeric.
* Send the payload!
* Having a shell is possible: /bin/sh
* Need to redirect stdout to stderr : `exec 1<&2`
* Demo!

## First flag found

    $ ls
    -rw-rw-r-- 1 pastebin pastebin   2403 Mar 12 15:50 av.c
    -rwxrwxr-x 1 cia      cia         143 Mar 10 15:09 ciaMalware.sh
    -rwxr-xr-x 1 root     root         42 Mar 13 20:07 cia.sh
    -r--r--r-- 1 ciaCTF   ciaCTF       54 Mar 10 15:11 flag.txt
    -rw-r--r-- 1 root     root        138 Mar 12 15:15 gccLine.txt
    -rw------- 1 root     root         76 Mar 12 18:25 .gdb_history
    -r-------- 1 ciaCTF   ciaCTF       27 Mar 13 20:10 hard_flag.txt
    -rwsr-sr-x 1 root     ciaCTF   743516 Mar 12 18:33 mine2
    -rw-r--r-- 1 root     root         20 Mar 12 18:25 peda-session-mine.txt

    $ id
    uid=1003(cia) gid=1002(ciaCTF) groups=1002(ciaCTF)

## Hard flag
There is another flag file which requires correct ciaCTF user privilege. 
Need to exploit the service itself to keep the correct level.

## Exploiting scanf
This seem exploitable but need more context. Having a shell, we can retrieve 
the binary and gccLine.txt help to understand the protection on the binary. 
In this case: executable stack with no canary and no ASLR.

When exploiting a stack overflow it is easier to fully control the stack. 
In this case, it is easier to call the binary directly on the server (using 
env) so we control exactly the layout of the stack and therefore the address 
of our payload.

In gdb: `unset env`. On execution: `env -i PWD=/home/pastebin/cia...`

* With an (almost) empty env, can use the cyclic helper to generate a 
  De Bruijn sequence. 
* We then know the exact offset of where saved-eip is. 
* Reuse shellcraft for cat a file. 
* Using fit() put our payload and buffer addr at the exact place.

## Root access

The setreuid is not quite right. `setreuid(USER_CIA_CTF,0); <- 0 == root`
That is the effective user id stays root. Even by using CIA as effective uid, 
the saved-uid would still be root. We can exploit that an re-elevate our 
privilege to root. To do so, just need to call setreuid in our payload.

* Fun with execve syscall (0xb) being a vertical tab. 
* Had to move payload higher on the stack to avoid stack usage overwritting 
  payload content

Thanks pastebin for a fun level!
