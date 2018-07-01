### Flag In A Haystack

I used this Perl one-liner to remove all alphanumeric characters:

    cat haystack.txt | perl -ple 's/[a-zA-Z0-9]//g'

### tomasz.7zz7.zsamot

As suggended by the name, I used ruby one-liner to reverse bytes in the file:

   open("x.7z", "wb").write open("tomasz.7zz7.zsamot", "rb").read.reverse

Then I unpacked it and read the flag from the picture.

### Warming up

It was just base64 followed by rotN. I used https://www.rot13.com/ to get the right rotation quickly.

### Nihilism

I uncommented `print(ciphertext)` from the cracker and got an array of numbers, with 24 different values.

I converted them to unique letters with this script:

    ct = [52, 32, 11, 31, 32, 41, 11, 31, 23, 24, 34, 13, 25, 15, 14, 13, 21, 33, 23, 11, 12, 32, 12, 11, 31, 23, 24, 42, 34, 34, 42, 52, 32, 41, 25, 43, 31, 14, 13, 12, 23, 52, 31, 13, 11, 22, 42, 23, 12, 41, 11, 33, 32, 34, 34, 45, 12, 35, 13, 33, 23, 12, 45, 12, 12, 11, 14, 42, 41, 25, 23, 14, 43, 13, 12, 12, 32, 51, 23, 41, 32, 31, 32, 34, 32, 12, 35, 32, 12, 12, 54, 35, 43, 11, 42, 35, 13, 11, 32, 21, 42, 24, 22, 23, 21, 14, 23, 13, 12, 23, 22, 22, 23, 21, 34, 32, 41, 23, 22, 14, 23, 21, 23, 22, 23, 22, 43, 42, 52, 23, 14, 42, 24, 11, 31, 23, 12, 43, 32, 14, 32, 11, 42, 41, 23, 14, 23, 21, 42, 25, 41, 32, 12, 23, 12, 11, 31, 13, 11, 13, 34, 34, 23, 53, 11, 23, 14, 41, 13, 34, 51, 13, 34, 45, 23, 12, 13, 14, 23, 23, 35, 43, 11, 54, 13, 41, 22, 31, 13, 51, 23, 41, 42, 11, 14, 45, 23, 13, 45, 11, 31, 42, 14, 32, 11, 54, 11, 31, 32, 12, 14, 23, 41, 22, 23, 14, 12, 11, 31, 23, 32, 41, 11, 23, 14, 41, 13, 34, 51, 13, 34, 45, 23, 12, 11, 31, 23, 21, 42, 41, 12, 21, 32, 23, 41, 21, 23, 35, 23, 13, 41, 32, 41, 25, 34, 23, 12, 12, 13, 12, 52, 23, 34, 34, 14, 23, 12, 45, 34, 11, 32, 41, 25, 32, 41, 11, 31, 23, 34, 42, 12, 12, 42, 24, 43, 23, 14, 12, 42, 41, 13, 34, 13, 45, 11, 31, 42, 14, 32, 11, 54, 13, 34, 34, 13, 45, 11, 31, 42, 14, 32, 11, 54, 25, 42, 41, 23, 11, 31, 23, 12, 43, 32, 14, 32, 11, 32, 41, 31, 42, 43, 23, 34, 23, 12, 12, 41, 23, 12, 12, 13, 41, 22, 52, 32, 11, 31, 13, 12, 23, 41, 12, 23, 42, 24, 24, 13, 11, 13, 34, 32, 12, 35, 12, 11, 14, 32, 51, 23, 12, 11, 42, 14, 32, 22, 32, 11, 12, 23, 34, 24, 42, 24, 13, 34, 34, 14, 23, 12, 43, 42, 41, 12, 32, 15, 32, 34, 32, 11, 54, 13, 34, 34, 11, 14, 45, 12, 11, 32, 41, 12, 42, 21, 32, 23, 11, 54, 32, 12, 25, 42, 41, 23, 13, 41, 22, 11, 31, 23, 52, 32, 34, 34, 32, 12, 52, 23, 13, 33, 23, 41, 23, 22, 13, 32, 35, 12, 35, 42, 11, 32, 51, 23, 12, 13, 41, 22, 25, 42, 13, 34, 12, 13, 14, 23, 25, 42, 41, 23, 11, 31, 23, 12, 43, 32, 14, 32, 11, 52, 13, 41, 11, 12, 12, 42, 35, 23, 11, 31, 32, 41, 25, 11, 42, 22, 23, 43, 23, 41, 22, 42, 41, 15, 45, 11, 31, 13, 12, 13, 15, 12, 42, 34, 45, 11, 23, 34, 54, 41, 42, 11, 31, 32, 41, 25, 11, 31, 13, 11, 32, 12, 41, 11, 13, 14, 15, 32, 11, 14, 13, 14, 54, 22, 32, 12, 32, 41, 11, 23, 25, 14, 13, 11, 32, 42, 41, 42, 24, 11, 31, 23, 12, 11, 14, 45, 21, 11, 45, 14, 23, 22, 12, 54, 12, 11, 23, 35, 42, 24, 51, 13, 34, 45, 23, 12, 34, 23, 13, 22, 12, 42, 41, 23, 11, 42, 12, 23, 23, 33, 23, 12, 21, 13, 43, 23, 32, 41, 13, 41, 54, 11, 31, 32, 41, 25, 11, 31, 13, 11, 12, 11, 32, 34, 34, 35, 13, 32, 41, 11, 13, 32, 41, 12, 13, 41, 42, 45, 11, 52, 13, 14, 22, 12, 23, 35, 15, 34, 13, 41, 21, 23, 42, 24, 13, 45, 11, 31, 42, 14, 32, 11, 54, 11, 31, 23, 12, 23, 11, 31, 32, 41, 25, 12, 13, 14, 23, 31, 42, 34, 34, 42, 52, 23, 12, 21, 13, 43, 23, 12, 11, 31, 42, 45, 25, 31, 52, 31, 13, 11, 41, 32, 23, 11, 55, 12, 21, 31, 23, 21, 13, 34, 34, 12, 12, 23, 34, 24, 41, 13, 14, 21, 42, 11, 32, 55, 13, 11, 32, 42, 41, 11, 31, 23, 12, 43, 32, 14, 32, 11, 13, 11, 11, 23, 35, 43, 11, 12, 11, 42, 23, 12, 21, 13, 43, 23, 42, 14, 13, 11, 34, 23, 13, 12, 11, 24, 42, 14, 25, 23, 11, 13, 15, 42, 45, 11, 11, 31, 23, 23, 35, 43, 11, 32, 41, 23, 12, 12, 11, 31, 23, 52, 23, 13, 33, 23, 41, 23, 22, 52, 32, 34, 34, 12, 11, 14, 32, 51, 23, 12, 11, 42, 32, 41, 11, 42, 53, 32, 21, 13, 11, 23, 32, 11, 12, 23, 34, 24, 32, 41, 14, 23, 12, 32, 25, 41, 13, 11, 32, 42, 41, 25, 23, 41, 23, 14, 13, 34, 32, 12, 13, 11, 32, 42, 41, 12, 43, 23, 11, 11, 54, 11, 31, 32, 41, 25, 12, 22, 23, 15, 13, 45, 21, 31, 23, 14, 54, 13, 41, 22, 24, 13, 41, 13, 11, 32, 21, 32, 12, 35, 11, 31, 23, 52, 32, 34, 34, 32, 12, 52, 23, 13, 33, 13, 41, 22, 12, 23, 23, 33, 12, 23, 12, 21, 13, 43, 23, 14, 13, 11, 31, 23, 14, 11, 31, 13, 41, 13, 21, 11, 32, 42, 41, 15, 45, 11, 13, 41, 54, 13, 11, 11, 23, 35, 43, 11, 11, 42, 23, 12, 21, 13, 43, 23, 41, 32, 31, 32, 34, 32, 12, 35, 52, 32, 11, 31, 42, 45, 11, 14, 23, 51, 13, 34, 45, 13, 11, 32, 41, 25, 51, 13, 34, 45, 23, 12, 42, 41, 34, 54, 35, 13, 33, 23, 12, 11, 31, 23, 43, 14, 42, 15, 34, 23, 35, 35, 42, 14, 23, 13, 21, 45, 11, 23]
    a="a"
    ht={}
    puts ct.map{|x| ht[x] || (ht[x] = a = a.next) }.join

And then used https://quipqiup.com/ to solve it.

### Flags on the Blockchain

The description mentioned IOTA blockchain, so I found a website with its data and searched for https://thetangle.org/tag/SECTALKS

There was one matching transaction - https://thetangle.org/transaction/UTCXNEPRCCDWLIIUEYUMFELGWINASGWRXIKXHFYPHTIMYUVIGHDXIVDJFPNFXZZJOTMQCJBHETRVA9999 - and it had 625 associated 0s and 1s, so I decided to print it as 25x25 block.
It looked vaguely like QR code, so I saved it to a PNM file:

    u = "0000000100010000010000000011111010001110101011111001000101010011001101000100100010100101000010100010010001011111100001010001001111101011000011101111100000000101010101010000000111111111011010111111111100110001111011110110100000000011010010010000101111111101011110010001100101101000010110011100011110011111100001010111000111001010001100011101011100011111001101101110100001011111101001101110100001111000000010000010011100000000011111111001100100111010110000000110100011010101111011111010010010001110101101000101000011110000011110100010110101011100111100010001011000001110101110101111101010111000110110010000000101011110100100000"
    xxx = "P6\n25 25\n255\n" + u.chars.map{|x| x == "0" ? [0,0,0] : [255,255,255]}.flatten.pack("C*")
    open("lol2.pnm", "wb"){|fh| fh.write(xxx)}

To get it recognized by QR reader I had to add padding:

    convert -extent 50x50 -gravity center  lol2.png lol2a.png

And then it all worked.

### Lucky Number

I modified the sources by inserting:

    printf("%d\n", (random ^ 0xBADA55));

before the check, and compiled it on another Linux machine (tried OSX first, but its `rand` returned different results).

### Python as a Service

Since ban list was baned on regexp, I used `__builtins__` to go around it,:

    i = __builtins__['__imp'+'ort__']
    os = i('os')
    sys = i('sys')
    sp = i('sub'+'process')

And then various commands to figure out what's going on, eventually getting to:

    print(getattr(os, 'environ'))
    print(getattr(os, 'listdir')('/etc'))
    co = getattr(sp, 'check_output')
    print(co(["git", "log", "-p"]))

The flag was in git logs.

### Linux Reversing I

I just used `strings` program to get the flag:

    strings 1 | grep flag

### Linux Reversing II

I just disassembled the file with:

    objdump -d ./2

and noticed long block of instructions like `cmp $0x7d,%al`, which checked one character at time.
I copied them all, and converted those hex numbers to ASCII characters to get the flag.

### Linux Reversing III

I used `gdb` to attach to the file and (Hopper would work a lot better), and get some idea what's going on.

The file was reading the flag, doing something to it, and `strncmp`ing it against something flag-like.

Based on first few characters and what was in disassembly I guessed it xors each `i`-th character with number `i`, so I did the same:

    # u = modified flag
    (0..32).map{|i| (u[i].ord ^ i).chr }.join

### Linux Reversing IV

I used Hopper demo version to decompile it, and noticed that answer starts with `157991`.
So I tried all numbers like that:

    for i in `seq 1579910000 1579919999`; do echo $i; echo $i | ./4 ; echo ; done

### Linux Reversing V

I used Hopper demo version to decompile it, and noticed a lot of checks which did some math to ecx and checked the results. I copied them to a z3 script.

I added some helpers (`>>` and `HIDWORD`) as I wasn't sure what it means exactly (signed / unsigned), and with helpers I could more easily flip that. I just made everything 64 bit to avoid extending variables and shrinking them back. That's not always perfect way, but in this case it worked just fine.

It's possible to clean it up a bit more.

    require "z3"

    class Z3::BitvecExpr
      def >>(o)
        self.unsigned_rshift(o)
      end
    end

    def HIDWORD(x)
      x.unsigned_rshift(32)
    end

    solver = Z3::Solver.new
    ecx = Z3::Bitvec("ecx", 64)

    solver.assert !(ecx - ((ecx - HIDWORD(ecx * 0x3ce4585) >> 0x1) + HIDWORD(ecx * 0x3ce4585) >> 0x9) * 0x3f1 != 0x34)
    solver.assert !(ecx - (HIDWORD(ecx * 0x8163d283) >> 0x9) * 0x3f5 != 0x266)
    solver.assert !(ecx - ((ecx - HIDWORD(ecx * 0x14191f7) >> 0x1) + HIDWORD(ecx * 0x14191f7) >> 0x9) * 0x3fb != 0x222)
    solver.assert !(ecx - ((ecx - HIDWORD(ecx * 0xc0906d) >> 0x1) + HIDWORD(ecx * 0xc0906d) >> 0x9) * 0x3fd != 0x274)

    p solver.satisfiable?
    p solver.model

Z3 found the solution for me.
