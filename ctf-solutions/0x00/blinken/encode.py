#!/usr/bin/python
import sys

strings = [
"defg`abclmnohijktuvwpqrs-}~ xyz{DEFG@ABCLMNOHIJKTUVWPQR",
"srqpwvut{zyx ~}-cba`gfedkjihonmlSRQPWVUT",
"tuvwpqrs-}~ xyz{defg`abclmnohijkTUVWPQRS",
"onmlkjihgfedcba` ~}-{zyxwvutsrqpONMLKJIM",
"a`cbedgfihkjmlonqpsrutwvyx{z}- ~A@CBEDGF",
]

inp = sys.argv[1]
for i in range(len(inp)):
	u = strings[i % 5]
	print str(u.find(inp[i])) + ", ",
