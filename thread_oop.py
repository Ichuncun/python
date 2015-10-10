#!/usr/bin/env python
import os
import time
import threading as t

def do():
	time.sleep(0.5)

class BootThread(t.Thread):
	def __init__(self, tid, monitor):
		self.tid = tid
		self.monitor = monitor
		t.Thread.__init__(self)
	def run(self):
		while True:
			monitor['lock'].acquire()
			if monitor['tick'] != 0:
				monitor['tick'] -= 1
				print(self.tid,":new left:",monitor['tick'])
				do()
			else:
				print("tid:",self.tid,"no more tickets")
				os._exit(0)
			monitor['lock'].release()
			do()

monitor = {'tick':100, 'lock':t.Lock()}

for k in range(10):
	new_thread = BootThread(k, monitor)
	new_thread.start()
