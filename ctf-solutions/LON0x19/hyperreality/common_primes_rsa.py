import os 
from rsalib import *

def extract(lines):
    return int(lines[0].strip().replace('n=',''))

e = 65537

with open('rsa_rng/alice.key') as f:
    alice = f.readlines()

alice_n = extract(alice)

for filename in os.listdir('rsa_rng'):
    if filename.endswith(".key") and not filename.startswith("alice"): 
        with open('rsa_rng/'+filename) as f:
            current_n = extract(f.readlines())
            factors = egcd(alice_n, current_n)
            if factors[0] != 1:
                print(filename)
                print(factors)
                p = factors[0]

with open('rsa_rng/message.txt.enc') as f:
    ct = int(f.read().strip())

q = alice_n // p

# print("n")
# print(alice_n)
# print("p")
# print(p)
# print("q")
# print(q)

phi = (p - 1) * (q - 1)
d = modinv(e, phi)

plaintext = pow(ct, d, alice_n)
print(bin_to_str(int_to_bin(plaintext)))

