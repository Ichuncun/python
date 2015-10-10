#!/usr/bin/env python
import os
import time
import threading as t

def do():
	time.sleep(0.5)

def boot(tid):
	global i
	global lock
	while True:
		lock.acquire()
		if i != 0:
			i -= 1
			print(tid,":new left:",i)
			do()
		else:
			print("tid:",tid,"no more tickets")
			os._exit(0)
		lock.release()
		do()

i = 100
lock = t.Lock()

for k in range(10):
	new_thread = t.Thread(target=boot,args=(k,))
	new_thread.start()
