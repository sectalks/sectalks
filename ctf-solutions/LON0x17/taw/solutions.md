
## bacon 1

The challenge already said it was encoded as upper/lower case characters.

    puts "0000 100000 100 0100001 0010 01 00010011 100000 10010 10 0110 01110 0100 000 1110 0011 0 1000 0110 10 01 0"
      .tr(" ", "")
      .scan(/.{5}/)
      .map{|x| (x.to_i(2) + 'a'.ord).chr }
      .join

## bacon 2

It was like first cipher, except with Unicode/ASCII characters as 1/0s. The difficulty was that spaces were supposed to be removed, but punctuation and newlines were supposed to stay.

    data = open("d/sectalks_2018_08/challenges/letter.txt", "rb").read
    puts data
      .scan(/[^ ]/)
      .join
      .unpack("U*")
      .map{|c| c > 256 ? 1 : 0}
      .join
      .scan(/.{5}/)
      .map{|u| u.to_i(2) }
      .map{|x| x + 'a'.ord }
      .map(&:chr)
      .join

## agent v1

I used ltrace to figure out what the program is trying to do:

    ltrace ./agent_secure_system_v1 password

It showed interesting line:

    strcmp("password", "agent.smith")

So changing command to:

    ltrace ./agent_secure_system_v1 agent.smith

Revealed the flag.

## agent v2

Similar ltrace approach showed that it's setting environment variable with `setenv` and then checking it with `getenv`.

It then revealed that it's using `getlogin` function to get current user.

So I wrote cheat.c:

    #include <stdio.h>

    int setenv(const char *name, const char *value, int overwrite) {
      return 0;
    }

    char *getlogin(void) { return "agent.smith"; }

It would return our fake login information, and also ignore all `setenv` codes.

I compiled it with:

    gcc -shared -fPIC  cheat.c  -o cheat.so

Then:

    LD_PRELOAD=`pwd`/cheat.so agent_term_secure=secureseedvalueplacement ltrace ./agent_secure_system_v2  agent.smith

Revealed the flag.

## JES v1

Like most ciphers it was completely reversible, so I just reversed order of operations and ran it backwards.


    def encrypt_block(self, b):
      for j in range(0, self.rounds):
        b = self.shiftRows(self.substituion(self.addkey(b)))
      return b

Became:

    def decrypt_block(self, b):
      for j in range(0, self.rounds):
        v = b
        vcopy = bytearray(v)
        w = self.unshiftRows(v)
        wcopy = bytearray(w)
        if self.shiftRows(wcopy) != vcopy:
          raise Exception("FAIL 1")

        u = self.unsubstituion(v)
        if self.substituion(u) != v:
          raise Exception("FAIL 2")

        w = self.unaddkey(u)
        if self.addkey(w) != u:
          raise Exception("FAIL 3")

        b = w
      return b

etc. I even checked that all reverse conversion are ok by instantly trying to redo the original.

### inject.bin

I googled the name, it was something about duck encoder, so I got a "duck decoder" from https://raw.githubusercontent.com/JPaulMora/Duck-Decoder/master/DuckDecoder.py and use that.

### archive

I simply unpacked it, then ran:

    for i in `seq 10`; do rename 's!/!-!' */*; rmdir */; done
    
A lot of times. A few times I manually renamed the folders due to max file name problem. There's better ways, but it was good enough.
