#! /usr/bin/env python3
# coding:utf-8

from kazoo.client import KazooClient
from kazoo.client import KazooState
from time import time
from time import sleep

zk = KazooClient(hosts="10.10.80.225:2781, 10.10.80.16:2781, 10.10.80.35:2781")
#zk = KazooClient(hosts="10.10.80.225:2181")
zk.start()
print(zk.state)
t0 = time()
num = 10000
for i in range(num):	
	try:
		zk.create("/test/", value=b"xxxxx", sequence=True)
	except Exception as e:
		print("reason:{}".format(e))
		t2 = time()
		while 1:
			sleep(1)
			try:
				#zk.start()
				zk.create("/test/", value=b"xxxxx", sequence=True)
			except Exception as e:
				print("reason:{}".format(e))
			else:
				t3 = time()
				print("zk server recovery, used:{}".format(t3 - t2))
				break
		

t1 = time()
print("create {} node, t1:{}, t0:{}, used:{}".format(num, t1, t0, t1 - t0))

zk.stop()
print(zk.state)
zk.close()

