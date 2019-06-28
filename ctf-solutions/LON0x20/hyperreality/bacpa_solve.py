import socket
import struct
import string
import binascii

from chosen_plaintext import ChosenPlaintext

HOST = 'c.ctf.turtleturtleup.com'
PORT = 1341

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


def send_blob(s, data):
    s.sendall(struct.pack('<I', len(data)))
    s.sendall(data)
    return


def recv_blob(s):
    data = s.recv(4)
    length, = struct.unpack('<I', data)

    data = ''
    while len(data) < length:
        newdata = s.recv(length - len(data))
        if newdata == '':
            raise Exception('connection closed?')
        data += newdata

    return data


class Client(ChosenPlaintext):

    def __init__(self):
        self.iv = s.recv(16)
        ChosenPlaintext.__init__(self, use_predicted_iv=True)
        return

    def IV(self):
        return self.iv

    def ciphertext(self, plaintext):
        send_blob(s, plaintext)
        data = recv_blob(s)

        print len(data),
        print self.plaintext

        self.iv = data[-16:]

        return data[16:]


c = Client()
c.run()
