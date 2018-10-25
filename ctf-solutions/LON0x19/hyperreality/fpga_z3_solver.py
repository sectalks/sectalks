from z3 import *
import re

s = Solver()

with open('gates.txt') as f:
    gates = [[int(b) for b in a.split()] for a in f.readlines()]

n = [Bool("%s" % (i + 1)) for i in range(4096)]

for g in gates:
    s.add(n[g[0]] == (Not(And(n[g[1]], n[g[2]]))))

s.add(n[1024] == True)

if s.check() == sat:
    m = s.model()
    sols = sorted([(d, m[d]) for d in m], key=lambda x: int(str(x[0])))
    binary = ''.join([str(int(str(a[1]) == "True")) for a in sols])
    eights = [chr(int(a[::-1], 2)) for a in re.findall('.{8}', binary[:512])]
    print(''.join(eights))
else:
    print(":(")
