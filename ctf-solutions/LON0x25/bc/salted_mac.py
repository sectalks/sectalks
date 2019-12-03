import json
import socket


def login(cookie):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('mtg.wtf', 9001))
        sock.sendall(b"login\n")
        sock.sendall(cookie.encode())
        sock.sendall(b"\n")
        line = ''
        while 'Goodbye!' not in line:
            line += sock.recv(512).decode()
        for line in line.strip().split("\n")[6:]:
            print(line)

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('mtg.wtf', 9001))
        # Sign ndmin=yes
        sock.sendall(b"sign\ndmin=yes\n")
        line = b''
        while b'}' not in line:
            line += sock.recv(512)
        (line,) = (l for l in line.split(b"\n") if l.startswith(b"Cookie"))
        signed = json.loads(line[len("Cookie: "):])
        if signed["salt"].endswith("a"):
            # Got salt which ends in 'a'
            print('')
            spoofed = json.dumps(dict(
                msg="admin=yes",
                salt=signed["salt"][:-1],
                mac=signed["mac"],
            ))
            print(spoofed)
            login(spoofed)
            exit(0)
        print(".", end="")
