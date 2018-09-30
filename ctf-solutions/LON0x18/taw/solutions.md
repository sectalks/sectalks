### tftp

Manually collect 30 characters. ROT13 them.

### haystack

Using [`binwalk`](https://github.com/ReFirmLabs/binwalks) and [`dedup_files`](https://github.com/taw/unix-utilities).

### 23andze

See attached program `pcap3_analyze`

### math_class

See attached program `math_class`

### ascii

See attached program `ascii`

### proof_of_work

See attached program `proof_of_work`

### bewf

I didn't finish this one.

I smashed stack with patterns like `abcdefghijklmnopqrstuvwxyz` all over to figure out alignment of return address overwrite.

```
ruby -e 's="\x08\x04\xf2\xe0".b.reverse; puts "dddd" + "z"*(76-4) + s '  | strace -f ./bewf
```

I tried returning to various standard library funcitons like `system`, but it never quite worked. For example there was `/bin/sh` in the binary, but its address had a whitespace in it, so it killed `scanf`.

Apparently there was already a premade function doing what I needed. Oh well, maybe next time.
