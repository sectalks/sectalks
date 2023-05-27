1. Discover `/code` endpoint from html comment
2. observe command injection potential
3. obsere use of shared regexp object, with global flag
4. exploit command injection by submitting enough payloads to flood global match
5. read flag.txt `http://localhost:5005/compress?query=%27;cat%20flag.txt)%23`