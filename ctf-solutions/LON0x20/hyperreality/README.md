## LON0x20 BACPA

AES is a secure cipher but is AES-CBC a secure cryptosystem? This challenge teaches us how a simple implementation error involving the Initialisation Vector (IV) can lead to total breakdown of an AES-CBC cryptosystem.

#### The challenge

We are given server source code in Go (`main.go`), and a port on which the server is listening. Connecting briefly, we see the server sends us some bytes and leaves the connection open, but doesn't appear to respond to anything we type.

Investigating the source code, we find:
 1. The server on initialisation creates a new AES cipher object with a 32-byte key and 16-byte blocksize.
 1. On receiving a connection, 16 random bytes are generated and sent to the client; this is the IV for the cipher.
 1. The first four bytes of the client input is read (as a little-endian 32-bit unsigned int) to determine the length of the input buffer.
 1. The input buffer is read, prepended to the flag and AES-CBC encrypted using the aforementioned key and IV, and the ciphertext is sent to the client.
 1. The IV for the next block is the last block of the ciphertext.

#### CCA2

These steps describe a ['blockwise-adaptive chosen-plaintext' scenario](https://link.springer.com/content/pdf/10.1007/3-540-45708-9_2.pdf), in which an attacker is able to retrieve the encryptions of arbitrary plaintexts, and after receiving the ciphertext of one block, 'adapt' an attack by&mdash;in this case&mdash;submitting another block under the same key and known IV. An attacker can use this to compromise a secret being appended to their plaintext.

#### The attack

First, a referesher of CBC mode of encryption:
![CBC mode of encryption](CBC_encryption.png)

That is:

![](https://latex.codecogs.com/svg.latex?C_{i}=E_{k}(P_{i}%20\oplus%20C_{i-1}),)

![](https://latex.codecogs.com/svg.latex?C_{0}%20=%20IV)

The IV exists to ensure that the same key + plaintext does not encrypt to the same ciphertext. If it did, then we could potentially decrypt somebody else's ciphertext by getting our plaintext guesses encrypted and seeing if we received ciphertexts that matched it.

The IV is not supposed to be reused, but in the case, we (as the attacker) are given the IV that will be used to encrypt the next message. This allows us to 'cancel out' the IV in successive decryptions, and verify guesses of what each character in the appended secret is.

Imagine we just sent the string `abcdefghijklmno` to be encrypted. That's 15 characters long so we know the first 15 characters of the block, and the 16th byte will be the added secret. From the server we receive blocks ![](https://latex.codecogs.com/svg.latex?C_{i}=C_{1},...,C_{j}), and note that ![](https://latex.codecogs.com/svg.latex?C_{j}) is the next IV. We want to verify if the letter `x` was the secret appended to our plaintext.

We now send ![](https://latex.codecogs.com/svg.latex?P^{*}%20\oplus%20C_{j}%20\oplus%20C_{j-1}) as the plaintext to be encrypted, where ![](https://latex.codecogs.com/svg.latex?P^{*}) is our guess (`abcdefghijklmnox`). Look what happens to the first ciphertext block we receive:

![](https://latex.codecogs.com/svg.latex?C%27_{1}=E_{k}(P%27_{1}%20\oplus%20C_{j}))

![](https://latex.codecogs.com/svg.latex?C%27_{1}=E_{k}((P^{*}%20\oplus%20C_{j}%20\oplus%20C_{j-1})%20\oplus%20C_{j}))

![](https://latex.codecogs.com/svg.latex?C%27_{1}=E_{k}(P^{*}%20\oplus%20C_{j-1}))

We already know that ![](https://latex.codecogs.com/svg.latex?C_{j}=E_{k}(P_{j}%20\oplus%20C_{j-1})), from the previous encryption.

So iff ![](https://latex.codecogs.com/svg.latex?P^{*}%20=%20P_{j}), then ![](https://latex.codecogs.com/svg.latex?C%27_{1}%20=%20C_{j})! Essentially, we have validated that `abcdefghijklmnox` was indeed the plaintext of the originally encrypted block, and `x` must be the appended secret.

To compromise longer secrets, we leak known secret characters one at a time into our attacking block, and guess every possible byte of the 16th slot only. By iteratively following this attack strategy, we learn the entire secret.

To prevent this attack, a new IV should be generated for each encryption. Interestingly, the attack is cipher-agnostic, and works equally as well regardless of whether DES, AES or Twofish is used. It's an attack against the broken block cipher mode rather than the cipher.

#### Attack implementation

During the CTF I was lazy and found a GPL-licensed pre-existing implementation of the attack, `chosen_plaintext.py` ([source](https://github.com/EiNSTeiN-/chosen-plaintext/blob/master/src/chosen_plaintext.py)). All that was required was to code the wrapper script to read and write the bytes on the wire, which can be found in `bacpa_attack.py`.
