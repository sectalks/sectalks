Run the executable in gdb `gdb from_future_import_flag_linux`.

```
(gdb) break *main
Breakpoint 1 at 0x400560
(gdb) r
Starting program: ......./from_future_import_flag_linux

Breakpoint 1, 0x0000000000400560 in main ()
```

We have now hit a breakpoint at the `main` function. Let's disassemble the function.

```
(gdb) disas
Dump of assembler code for function main:
=> 0x0000000000400560 <+0>:     sub    $0x98,%rsp
   0x0000000000400567 <+7>:     xor    %edi,%edi
   0x0000000000400569 <+9>:     mov    %fs:0x28,%rax
   0x0000000000400572 <+18>:    mov    %rax,0x88(%rsp)
   0x000000000040057a <+26>:    xor    %eax,%eax
   0x000000000040057c <+28>:    callq  0x400530 <time@plt>
   0x0000000000400581 <+33>:    mov    %rsp,%rdi
   0x0000000000400584 <+36>:    mov    %rax,(%rsp)
   0x0000000000400588 <+40>:    callq  0x400550 <gmtime@plt>
   0x000000000040058d <+45>:    cmpl   $0x77,0x14(%rax)
   0x0000000000400591 <+49>:    jle    0x4005b5 <main+85>
   0x0000000000400593 <+51>:    lea    0x8(%rsp),%rdi
   0x0000000000400598 <+56>:    callq  0x4006dd <reveal_password>
   0x000000000040059d <+61>:    lea    0x8(%rsp),%rdx
   0x00000000004005a2 <+66>:    mov    $0x400794,%esi
   0x00000000004005a7 <+71>:    mov    $0x1,%edi
   0x00000000004005ac <+76>:    xor    %eax,%eax
   0x00000000004005ae <+78>:    callq  0x400540 <__printf_chk@plt>
   0x00000000004005b3 <+83>:    jmp    0x4005c6 <main+102>
   0x00000000004005b5 <+85>:    mov    $0x400798,%esi
   0x00000000004005ba <+90>:    mov    $0x1,%edi
   0x00000000004005bf <+95>:    xor    %eax,%eax
   0x00000000004005c1 <+97>:    callq  0x400540 <__printf_chk@plt>
   0x00000000004005c6 <+102>:   xor    %eax,%eax
   0x00000000004005c8 <+104>:   mov    0x88(%rsp),%rcx
   0x00000000004005d0 <+112>:   xor    %fs:0x28,%rcx
   0x00000000004005d9 <+121>:   je     0x4005e0 <main+128>
   0x00000000004005db <+123>:   callq  0x400500 <__stack_chk_fail@plt>
   0x00000000004005e0 <+128>:   add    $0x98,%rsp
   0x00000000004005e7 <+135>:   retq
End of assembler dump.
```

There is a branch `jle` function. We want to be able to hit the `reveal_password` function at `0x400598` rather than jumping to `0x4005b5`.

We can't jump directy to the `reveal_password` function as we need the correct register values, so let's move the program counter to directly after the `jle`.

```
(gdb) set $pc=0x400593

(gdb) c
Continuing.
flag{...
```
