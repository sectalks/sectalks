1. Use netcat to grab the service banner on port 5000 `nc -v localhost 5000`
2. The service is ssh
3. The challenge name suggests the username is anonymous, try `anonymous:anonymous`
4. Try ssh and notice only sftp is enabled
4. Use sftp to list the files and read the `note` file