#!/usr/bin/env python
import os
import threading as t
import multiprocessing as p

def worker(sign, lock):
	lock.acquire()
	print(sign, os.getpid())
	lock.release()

print("Main:",os.getpid())

# multi thread 
record = []
lock = t.Lock()
for i in range(5):
	thread = t.Thread(target=worker,args=('thread',lock))
	thread.start()
	record.append(thread)

for thread in record:
	thread.join()

# multi process
record = []
lock = p.Lock()
for i in range(5):
	process = p.Process(target=worker,args=('process',lock))
	process.start()
	record.append(process)

for process in record:
	process.join()
