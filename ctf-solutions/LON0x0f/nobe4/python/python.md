---

title: Python
points: 20

---

This challenge involve some whitespaces at the end of the file, if you can't see them, use `:set list` on vim. And if you're not using vim, what are you waiting for?

The second line is building an list of all the lines length:

```python
DT=[len(w)-1 for w in open(__file__).readlines()]
```

It looks like it should prevent us from changing the file, but let's do something better:
I will add a `print DT` on the 4th line which original length is `0` so I can track it quite easily, then I save the content of the printed array and I can mess with the file.

The array is thus:
```python
DT = [21, 49, 10, 0, 18, 26, 20, 75, 20, 75, 20, 75, 20, 75, 20, 59, 20, 75, 20, 75, 20, 75, 20, 75, 20, 59, 20, 75, 20, 75, 20, 75, 20, 59, 20, 75, 20, 59, 20, 75, 20, 59, 20, 15, 0, 27, 56, 32, 29, 5, 31, 23, 5, 25, 30, 10, 22, 27, 18, 20, 26, 15, 13, 31, 32, 14, 19, 9, 29, 11, 4, 16, 6, 24, 3, 1, 7, 8, 28, 2, 17, 0, 12, 21]
```

Now the `DT` index is used to obfuscate the char comparisons, like:

```python
if ord(key[DT[67]]) - (DT[79]*DT[64]+DT[76]) != (DT[75]*DT[64]+DT[82])
```

Fortunately, we can reverse this process, the general idea is to transform:

```python
if ord(key[X]) - (Y) != (Z):
```

into

```python
print X, chr(Z + Y)
```

Here `X` is the index of the array and `chr(Z+Y)` its char. Let's use our vim-fu again:

Removing all lines that don't contain `DT`.
```vim
:v/DT/d
```
Manually removes the last two lines, it's checking the number of arguments and calling the validation.

Now the first print will be:

```python
print DT[58]
```

It's the size of the password.

Now let's bring up the big guns:

```vim
:%s/if ord(key\[\(DT\[..\]\)\]) - \([^!]\+\)!=\([^:]\+\):/print \1, chr(\3 + \2)
:%s/if ord(key\[\(DT\[..\]\)\]) + \([^!]\+\)!=\([^:]\+\):/print \1, chr(\3 - \2)
```

I'll explain what this does in a moment, what's interesting is the result when we run the file:

```vim
:r!python %
```

```python
18
9 s
4 i
14 l
8 i
6 g
13 i
5 n
1 i
2 s
10 h
12 b
3 t
17 y
16 t
11 a
0 d
15 i
7 u
```
We have our size (18) and all our chars in random order, let's sort that:

```vim
:sort
```

```
0 d
1 i
2 s
3 t
4 i
5 n
6 g
7 u
8 i
9 s
10 h
11 a
12 b
13 i
14 l
15 i
16 t
17 y
```

And we have our password:

> distinguishability

---

Note on Vim:

The two big commangs used above are using the same pattern, which is one of the most powerfull tool vim gives us.

`:%s/A/B/` will substitute on every line (that's what the `%` stands for) the `A` with the `B`.

`A` looks like:

```
if ord(key\[\(DT\[..\]\)\]) + \([^!]\+\)!=\([^:]\+\):
```

It's matchin the start of the line, escaping the `[` and `(` and creating a group: `\(DT\[..\]\)`, this will holds in memory this precise pattern, so we can use it in the later substitution. `DT\[..\]` will match the `DT` array with a 2-digits number. It's our `X`.

Then we're matching the closing brackets, the `+` (resp `-`) and creating another group: `\([^!]\+\)`.
This one will match everything that is *not* a `!` up until a `!` (or the end of the line). It's maching the `Y`.

Then, after matching the `!=` we're matching the last group, following the same logic: `\([^:]\+\)`. It's our `Z`.

`B` is:

```
print \1, chr(\3 + \2)
```

You remember the 3 groups we made, for `X`, `Y` and `Z`? We can use them as `\1`, `\2` and `\3`. So this should be clear now.

example:
```
if ord(key[DT[67]]) - (DT[79]*DT[64]+DT[76]) != (DT[75]*DT[64]+DT[82]):
print DT[67], chr( (DT[75]*DT[64]+DT[82]) + (DT[79]*DT[64]+DT[76]) )
```

> And if you're not using vim, what are you waiting for?
