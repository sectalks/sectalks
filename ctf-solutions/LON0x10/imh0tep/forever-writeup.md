# Forever Linux

## Main challenge

The challenge was a linux x64 binary file containing 3 flags.  The instructions indicated using `gdb` would be required.

First the obligatory run of `checksec`:

```
$ ./checksec.sh --file ./forever-linux
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   ./forever-linux
```

Thankfully there were few security mitigations (including ASLR) applied to the binary.

Breaking in `main` and stepping instruction by instruction indicated that the program was stuck in an infinite loop:

```
0x400ae0 <main+21>      mov    BYTE PTR [rbp-0x9],0x0
0x400ae4 <main+25>      cmp    BYTE PTR [rbp-0x9],0x1
0x400ae8 <main+29>      jne    0x400ae4 <main+25> 
```

Breaking at `*0x400ae4` and setting `[rbp-0x9]` to `1` (`set *(char*)($rbp-9)=1`) quickly bypasses this loop and gets us the first flag:

```
flag: When in doubt, say nothing and move on.
```

This leads us onto an input prompt asking for an activation code:

```
Enter activation code [XXXXXXXX]:
```

The `check_activation_code` function had a lot of complexity, so to get to the flag quickly it was easier to bypass the check completely.  Observing the assembly, the return code of the function is checked immediately upon return:

```
0x400c18 <main+333>     call   0x40084d <check_activation_code>
0x400c1d <main+338>     test   eax,eax
0x400c1f <main+340>     je     0x400c4f <main+388>
```

Breaking at `*0x400c1d` and setting `eax` to `0` (`set $eax=0`) gets past this and gives us the second flag:

```
flag: It has yet to be proven that intelligence has any survival value.
```

Next we hit a function called `THE_FINAL_COUNTDOWN`.  Stepping into this, some quick following of execution flow found the final check before the call to `print_flag` failing:

```
0x400a6c <THE_FINAL_COUNTDOWN+52>       cmp    al,0x2a
0x400a6e <THE_FINAL_COUNTDOWN+54>       jne    0x400a89 <THE_FINAL_COUNTDOWN+81>
0x400a70 <THE_FINAL_COUNTDOWN+56>       mov    esi,0x4d
0x400a75 <THE_FINAL_COUNTDOWN+61>       mov    edi,0x6020a0
0x400a7a <THE_FINAL_COUNTDOWN+66>       call   0x40097e <print_flag>
```

Breaking at `*0x400a6c` and setting `al` to `0x2a` (`set $al=0x2a`) gets past this and gives us the third flag:

```
flag: It was the mark of a barbarian to destroy something one could not understand.
```

This process can be emulated with the included gdb script `forever-script.gdb`.  Simply run the following command on 64-bit linux with both the binary and script file available:

```
$ gdb --batch -x forever-script.gdb ./forever-linux < <(echo 0) | grep flag
```

## Further work

### Activation Code

Following completion of this challenge, the next task was to reverse the activation code generator.  It was not possible to complete this in the allotted time, but did create a brute force tool in order to collect the first few activation codes in an attempt to observe the pattern: `forever-brute.py`.  This must be run against a binary with the first infinite loop patched out.  Once run it gave the following (truncated) output:

```
10000006 0x989686 0b100110001001011010000110
10000010 0x98968a 0b100110001001011010001010
10000012 0x98968c 0b100110001001011010001100
10000018 0x989692 0b100110001001011010010010
10000020 0x989694 0b100110001001011010010100
```

### Patcher

After the challenge was complete I wrote a small script to patch the binary and produce a file (`forever-linux-patched`) that would output the flags with no user interaction (apart from supplying a dummy activation code): `forever-patcher.py`.