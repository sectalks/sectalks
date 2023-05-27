1. You need to solve Anon first, in the note file you'll find out about a host name `filereader`
1. This service does not expose a port, however its accessible in docker-compose through the `proxy` container
1. Navigate to http://127.0.0.1:5004/proxy and set the "Host" header to `filereader`. Now you can access an internal app that reads local files
1. Notice a user named `flag` in `/etc/passwd`
1. Save the contents of `/etc/shadow` and `/etc/passwd`
1. Use unshadow to combine them `unshadow shadow passwd > pass`
1. Crack using `rockyou.txt` wordlist and john `john --wordlist /usr/share/wordlists/rockyou.txt pass`