#!/usr/bin/python

# Source: http://training.securitum.com/rozwal/starter/game.py.txt

import socket
import os, sys
import ast
import random

def write(msg):
  sys.stdout.write(msg)
  sys.stdout.flush()

def read(prompt=''):
  if prompt:
    write(prompt)
  return sys.stdin.readline().strip()

def loop():
  RANGE = 1000000
  num = read('Select a number in range (0, 10000000000000000000000): ')
  try:
    num = ast.literal_eval(num) + 0
    assert 0 < num < 10000000000000000000000
  except:
    write("Oops! You probably didn't enter a number or the number's not in the correct range!\n\n")
    return
  rand = num + int(random.random()*RANGE)
  guess = read('Now guess a number in range: [{:n}, {:n}]: '.format(num, num+RANGE))
  try:
    guess = ast.literal_eval(guess)
  except:
    write("Oops! You probably didn't enter a number!\n\n")
    return
  if guess == rand:
    write('Wow! The flag is: ')
    with open('/home/game/flag.txt', 'r') as f:
      write(f.read())
    sys.exit(0)
  write('Better luck next time!\n\n')  

def main():
  write('Hello there in "Guess the number!"\nYou have 30 seconds.\n')
  while True:
    loop()

main()

