# The Python version was super slow so I swapped out the bruteforcer for a C
# one...

gcc permuter.c -o permuter -lcrypto

python2 proof_of_work.py
