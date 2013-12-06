#!/usr/bin/python
#break9optimised.py
import sys
import itertools
import multiprocessing
from multiprocessing import Process, Queue
from string import ascii_lowercase
import time
def work(s):
    passcode = 1
    passtot = 0
    password = ''.join(s)
    for i, c in enumerate(password):
        passtot += (i*ord(c)*ord(c))
        passcode *= ord(c)
    if  ((passcode == 1842055687879732800) and (passtot == 393644)):
        return password
    else:
        return 0
def brute(s, queue):
    chars = ascii_lowercase
    while True:
        try:
            if not s.empty():
                q = s.get(block = False)
                z = multiprocessing.Queue()
                for i in itertools.product(chars,repeat=3):
                    z.put(i)
                while True:
                    try:
                        if not z.empty():
                            c = z.get()
                            for i in itertools.product(chars,repeat=3):
                                try:
                                    w = q+c+i
                                    res = work(w)
                                    if ("".join(c+i) == 'zzzzzz'):
                                        print ''.join(w)
                                    if (res != 0):
                                        queue.put((res))
                                except:
                                    pass
                        else:
                            break
                    except:
                        pass
            else:
                break
        except:
            pass
def write(queue, fname):
    fhandle = open(fname, "a")
    while not queue.empty():
        try:
            username = queue.get()
            print >>fhandle, username
        except:
            break
    fhandle.close()
def main():
    chars = ascii_lowercase
    nthreads = multiprocessing.cpu_count() 
    fname = "break9optimised-output.txt"
    print 'using: '+str(nthreads)+' threads'
    print 'outputting to: '+fname
    writerQueue = multiprocessing.Queue()
    workQueue = multiprocessing.Queue()
    writProc = Process(target = write, args = (writerQueue, fname))
    for e in itertools.product(chars,repeat=3):
        workQueue.put((e), block=False)
    print 'work loaded'
    workProc = [Process(target = brute , args = (workQueue, writerQueue)) for i in xrange(nthreads)]
    for p in workProc:
        p.start()
    for p in workProc:
        p.join()
    print 'write started'
    writProc.start()
    writProc.join ()
    print('done')
if __name__ == '__main__':
    main()
