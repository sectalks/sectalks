with open('hangul-flag.enc') as f:
    bla = f.read()

print(min([ord(b) for b in bla]))
print(max([ord(b) for b in bla]))
print(sorted(list(set(bla))))
print(len(set(bla)))

a = [chr((ord(b)-44032)//28) for b in bla]

print("".join(a))
