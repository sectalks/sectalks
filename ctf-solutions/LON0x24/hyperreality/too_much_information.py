# -*- coding: utf-8 -*-
from paddingoracle import BadPaddingException, PaddingOracle
from base64 import b64encode, b64decode
from urllib import quote, unquote
import requests
import socket
import time
import binascii
from pwn import *


class PadBuster(PaddingOracle):
    def __init__(self, **kwargs):
        super(PadBuster, self).__init__(**kwargs)
        self.session = requests.Session()
        self.wait = kwargs.get('wait', 2.0)

    def oracle(self, data, **kwargs):
        r = remote('35.177.74.111', 44021)

        ct = binascii.hexlify(data)

        r.recvline()
        print(r.recvuntil('IV: '))
        r.sendline('dc65088ee6374539')
        print(r.recvuntil('MESSAGE: '))
        print(ct)
        r.sendline(ct)
        r.recvline()
        res = r.recvline()
        print(res)
        r.close()

        if 'SUCCESS' in res:
            logging.debug('No padding exception raised on %r', ct)
            return
        # if 'ERROR' in res:
        #     print("error")

        print(self._decrypted)

        raise BadPaddingException


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level=logging.DEBUG)

    iv = binascii.unhexlify("dc65088ee6374539")
    message = binascii.unhexlify("c452e5feffa25f1c0dae6462642a396c5f476515bbd30f925e3dbbbe4e26a243c6c0f7d6b579c3ad71d766b3408218b46aeef31e8d991dc6163f5b0b39591202aad7ac723a554195")

    padbuster = PadBuster()

    flag = padbuster.decrypt(message, block_size=8, iv=iv)
    print('Decrypted flag: => %r' % flag)
