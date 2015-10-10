#!/usr/bin/env python
import os
import time
import multiprocessing as p

def inq(queue):
	info = str(os.getpid()) +"(put):" + str(time.time())
	queue.put(info)

def outq(queue,lock):
	info = queue.get()
	lock.acquire()
	print(str(os.getpid()) + "(get):" +info)
	lock.release()

record1 = []
record2 = []
lock = p.Lock()
queue = p.Queue()

for i in range(10):
	process = p.Process(target=inq,args=(queue,))
	process.start()
	record1.append(process)

for i in range(10):
	process = p.Process(target=outq,args=(queue,lock))
	process.start()
	record2.append(process)

for p in record1:
	p.join() 

queue.close()

for p in record2:
	p.join() 
