import string

# Not the prettiest function, but does the job
def rot_caesar_decrypt(message, n):
    result = ''
    ind = 'abcdefghijklmnopqrstuvwxyz'
    for j, word in enumerate(message.split()):
        for i, l in enumerate(word):
            # print word
            try:
                i = (ord(l) - 96) - (ord(key[j % len(key)]) - 96)
                result += ind[i % 26]
            except ValueError:
                result += l
        result += ' '
    return result

ciphertext = "ozz kagd hgyk ofs nqxazs zu ig"
key = "omg"
assert rot_caesar_decrypt(ciphertext, key) == "all your base are belong to us "

with open('ciphertext.txt', 'r') as f:
    ciphertext = f.read()

# Solved through a manual process made rather painful by the fact the first words are Vietnamese
# The breakthrough was to pick words nearer the middle until English started appearing
# for i in string.ascii_lowercase:
#     key = 'unsprinkled' + i
#     print(key + " " + rot_caesar_decrypt(ciphertext, key)[:80])

key = 'unsprinkled'
print(rot_caesar_decrypt(ciphertext, key))

