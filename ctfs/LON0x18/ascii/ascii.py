# socat -T30 -d -d TCP-LISTEN:6000,fork,reuseaddr EXEC:"python3 -u ascii.py",pty,echo=0
import sys
import string
import secrets
import uuid
import re

alphabet = []
alphabet.append('###########  #####    ###  ##  ##      ##  ##  ##  ##  #########')
alphabet.append('#########     ###  ##  ##     ###  ##  ##  ##  ##     ##########')
alphabet.append('##########    ###  ##  ##  ######  ######  ##  ###    ##########')
alphabet.append('#########    ####  #  ###  ##  ##  ##  ##  #  ###    ###########')
alphabet.append('#########      ##  ######    ####  ######  ######      #########')
alphabet.append('#########      ##  ######    ####  ######  ######  #############')
alphabet.append('##########    ###  ##  ##  ######  #   ##  ##  ###    ##########')
alphabet.append('#########  ##  ##  ##  ##      ##  ##  ##  ##  ##  ##  #########')
alphabet.append('##########    #####  ######  ######  ######  #####    ##########')
alphabet.append('###########    #####  ######  ######  ###  #  ####   ###########')
alphabet.append('#########  ##  ##  #  ###    ####    ####  #  ###  ##  #########')
alphabet.append('#########  ######  ######  ######  ######  ######      #########')
alphabet.append('#########  ###  #   #   #       #  # #  #  ###  #  ###  ########')
alphabet.append('#########  ##  ##   #  ##      ##      ##  #   ##  ##  #########')
alphabet.append('##########    ###  ##  ##  ##  ##  ##  ##  ##  ###    ##########')
alphabet.append('#########     ###  ##  ##  ##  ##     ###  ######  #############')
alphabet.append('##########    ###  ##  ##  ##  ##  ##  ###    #######  #########')
alphabet.append('#########     ###  ##  ##  ##  ##     ###  #  ###  ##  #########')
alphabet.append('##########    ###  ##  ##    #######   ##  ##  ###    ##########')
alphabet.append('#########      ####  ######  ######  ######  ######  ###########')
alphabet.append('#########  ##  ##  ##  ##  ##  ##  ##  ##  ##  ###    ##########')
alphabet.append('#########  ##  ##  ##  ##  ##  ##  ##  ###    #####  ###########')
alphabet.append('#########  ###  #  ###  #  # #  #       #   #   #  ###  ########')
alphabet.append('#########  ##  ##  ##  ###    ####    ###  ##  ##  ##  #########')
alphabet.append('#########  ##  ##  ##  ###    #####  ######  ######  ###########')
alphabet.append('#########      #####  #####  #####  #####  ######      #########')
alphabet.append('                                                                ')

dictionary = open("/usr/share/dict/words", encoding="utf-8").read().split()
dictionary = [re.sub(r'[^a-zA-Z ]+', '', w) for w in dictionary]

loop_count = 25
sentence_len = 2
tag = uuid.uuid4()

flag = 'STL{coordinated_spotless_amount}'

def output_sentence(s):
    sentence = []
    for c in s:
        if c.lower() in string.ascii_lowercase:
            sentence.append(alphabet[ord(c.lower()) - 97])
        elif c == ' ':
            sentence.append(alphabet[26])

    for i in range(8):
        print(' '.join(l[i*8:i*8+8] for l in sentence))

def main():
    print('Welcome to Ascii-Me')
    print('Send me some letters and I will ascii them.')
    print('Please only send letters and spaces.')
    print('After the asciination, you need to de-asciinate what I send you and send the normal letters back.')

    s = sys.stdin.readline().rstrip()
    sys.stderr.write('{} received {}\n'.format(tag, s))
    output_sentence(s)

    for i in range(loop_count):
        decode = ' '.join(secrets.choice(dictionary) for _ in range(sentence_len)).lower()
        sys.stderr.write('{} sending {} ({}/{})\n'.format(tag, decode, i+1, loop_count))
        output_sentence(decode)

        print('De-asciinate those letters... ({}/{})'.format(i+1, loop_count))
        s = sys.stdin.readline().rstrip()
        sys.stderr.write('{} received {} ({}/{})\n'.format(tag, s, i+1, loop_count))

        if s.lower() == decode:
            print('Thanks for asciinating!')
        else:
            print('Nope, you are not asciinating...')
            break
    else:
        sys.stderr.write('{} sending flag!\n'.format(tag))
        print(flag)
    
if __name__ == "__main__":
    main()