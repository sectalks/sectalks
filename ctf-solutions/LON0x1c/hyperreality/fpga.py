from z3 import *
import re

s = Solver()

gates = []

with open('challenge_files/gates.txt') as f:
    for a in f.readlines():
        gates.append([a.split()[0]] + [int(b) for b in a.split()[1:]])

n = [Bool("%s" % (i + 1)) for i in range(4096)]

for g in gates:
    if g[0] == "and":
        s.add(n[g[1]] == (And(n[g[2]], n[g[3]])))
    elif g[0] == "nand":
        s.add(n[g[1]] == (Not(And(n[g[2]], n[g[3]]))))
    elif g[0] == "or":
        s.add(n[g[1]] == (Or(n[g[2]], n[g[3]])))
    elif g[0] == "nor":
        s.add(n[g[1]] == (Not(Or(n[g[2]], n[g[3]]))))
    elif g[0] == "xor":
        s.add(n[g[1]] == (Xor(n[g[2]], n[g[3]])))

s.add(n[1024] == True)

if s.check() == sat:
    m = s.model()
    sols = sorted([(d, m[d]) for d in m], key=lambda x: int(str(x[0])))
    binary = ''.join([str(int(str(a[1]) == "True")) for a in sols])
    eights = [chr(int(a[::-1], 2)) for a in re.findall('.{8}', binary[:512])]
    print(''.join(eights))
else:
    print(":(")
