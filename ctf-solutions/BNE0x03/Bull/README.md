# BNE0x03 - Simple CTF Walkthough by Bull (@RobertWinkel)

1)	Find the IP address, e.g.:
```
root@kali:~# netdiscover -i eth1 -r 192.168.56.0/24

 Currently scanning: Finished!   |   Screen View: Unique Hosts                               
                                                                                             
 3 Captured ARP Req/Rep packets, from 3 hosts.   Total size: 180                             
 _____________________________________________________________________________
   IP            At MAC Address      Count  Len   MAC Vendor                   
 ----------------------------------------------------------------------------- 
 192.168.56.100  08:00:27:64:63:0f    01    060   CADMUS COMPUTER SYSTEMS                    
 192.168.56.101  08:00:27:00:c4:ae    01    060   CADMUS COMPUTER SYSTEMS                    
 192.168.56.102  08:00:27:60:21:5c    01    060   CADMUS COMPUTER SYSTEMS                    
```

2)	Find the services, e.g.:
```
root@kali:~# nmap -p- -sV -A 192.168.56.102

Starting Nmap 6.47 ( http://nmap.org ) at 2015-09-21 22:27 AEST
Nmap scan report for 192.168.56.102
Host is up (0.00049s latency).
Not shown: 65534 closed ports
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.7 ((Ubuntu))
|_http-methods: No Allow or Public header in OPTIONS response (status code 200)
|_http-title: Please Login / CuteNews
MAC Address: 08:00:27:60:21:5C (Cadmus Computer Systems)
Device type: general purpose
Running: Linux 3.X
OS CPE: cpe:/o:linux:linux_kernel:3
OS details: Linux 3.11 - 3.14
Network Distance: 1 hop

TRACEROUTE
HOP RTT     ADDRESS
1   0.50 ms 192.168.56.102

OS and Service detection performed. Please report any incorrect results at http://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.69 seconds
```
   Notice that there is only a web server running.

3)	Visit http://192.168.56.102 in a browser and see that CuteNews v2.0.3 is running.

4)	Search for CuteNews on an exploit site, e.g. www.exploit-db.com. Discover the remote file unload vulnerability and exploit (https://www.exploit-db.com/exploits/37474/). 

5)	Use exploit to get a reverse shell as user www-data.

6)	Do a uname -a and discover Ubuntu 14.04.1 is in use.

7)	Search for Ubuntu 14.04 on exploit site, e.g. www.exploit-db.com. Discover the overlayfs remote root shell exploit (https://www.exploit-db.com/exploits/37292/). 
   Note: Other potential exploits include https://www.exploit-db.com/exploits/37088/ and https://www.exploit-db.com/exploits/1518/

8)	Write the exploit code somewhere, e.g. /tmp/. Compile and execute.

9)	Grab /root/flag.txt.

10) Profit!
