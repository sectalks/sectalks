The challenge was a Linux binary, compiled with debugging information left in and compiler optimizations turned off. As first step I disassembled it with `objdump`.

I tried running it, but it got straight into infinite loop. I found code inside <main> for infinite loop, and used hex editing script to replace it with `NOP` sequence (`0x90`). That got the first flag.

After that the program asked for the activation code - I used same hex editing strategy to replace `JE` opcode (checking for equality) with `JNE` (checking for inequality). This got to the second flag.

Then I ran into a problem. The program was slightly self-modifying, so disassembled code I got was not what was actually running. I had to actually use disassembler, put a breakpoint in `THE_FINAL_COUNTDOWN` function, and edit it from within `gdb` - basically restoring it to what binary claimed should be the right code. That got me the final flag.

Then there was a followup challenge of writing keygen for activation code. None of decompilers I tried worked with 64bit code, and checking this function manually was too much work, so I wrote a simple C program:

    #include <stdio.h>
    #include <stdlib.h>

    int test(int x) {
      asm("nop");
      // 200x of those just to make some space
      asm("nop");
      return 0;
    }

    int main() {
      // 9999999
      for(int i=0; i<99999999; i++) {
          int res = test(i);
          if(res != 1)
            printf("%d %d\n", i, res);
      }
      printf("lol\n");
      return 0;
    }

And then replaced `test` function with one from the binary. Somehow it ran even though I was testing it on a different operating system. It generated a lot of valid keys, and there seemed to be some pattern. Unfortunately The On-Line Encyclopedia of Integer Sequences didn’t give me any exact answer.
