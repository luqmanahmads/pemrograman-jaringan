import threading
import time

def workerA():
	while True:
		print "A"
	return

def workerB():
	print "ini adalah B"
	time.sleep(1)
	return

def workerC():
	while True:
		print "C"
	return

threads = []

a=threading.Thread(target=workerA)
a.start()

b=threading.Thread(target=workerB)
b.start()

c=threading.Thread(target=workerC)
c.start()
