#!/usr/bin/env python
import multiprocessing as p

def proc(pipe):
	pipe.send("hello")
	print("proc rec:",pipe.recv())

def proc2(pipe):
	print("proc2 rec:",pipe.recv())
	pipe.send("hello, too")

pipe = p.Pipe()

p1 = p.Process(target=proc,args=(pipe[0],))
p2 = p.Process(target=proc2,args=(pipe[1],))

p1.start()
p2.start()

p1.join()
p2.join()
