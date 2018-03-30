#! /usr/bin/env python3
# coding:utf-8
import time 
import redis
import threading

class redis_client(threading.Thread):
	def __init__(self, name, base, count):
		threading.Thread.__init__(self)
		self.name = name
		self.base = base
		self.count = count

	def run(self):
		redis_connection = redis.StrictRedis(host="10.10.80.129", port=6381, password="wjp", decode_responses=True)
		#redis_connection = redis.StrictRedis(host="10.10.80.35", port=6382, password="wjp", decode_responses=True)
		#redis_connection = redis.StrictRedis(port=6382, password="wjp", decode_responses=True)
		t0 = time.time()
		size = self.base + self.count
		num = self.base
		while num < size:
			try:
				redis_connection.set(str(num), '{},xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'.format(self.name))
			except Exception as e:
				print('thread:{}, reason:{}, num:{}'.format(self.name, e, num))
				t3 = time.time()
				while 1:
					time.sleep(1)
					try:
						redis_connection.set(str(num), 'redis raise exception')
					except Exception as e:
						print('thread:{}, reason:{}, num:{}'.format(self.name, e, num))
					else:
						t4 = time.time()
						print("thread:{}, exception recovery spent:t4:{}, t3:{}, {}".format(self.name, t4, t3, t4-t3))
						break
			num = num + 1
		t1 = time.time()
		print("thread:%s, commond:set  %d frequency  start_time:%.3f, end_time:%.3f, used:%.3f" %(self.name, self.count, t1, t0, t1-t0))

def start():
	num = 0
	client_num=50
	size = 20000
	d = {}
	for x in range(client_num):
		d['redis_client_' + str(x)] = redis_client("thread-{}".format(x), num, size)
		d['redis_client_' + str(x)].start()
		num += size
		
	for x in range(client_num):	
		d['redis_client_' + str(x)].join()
		
if (__name__ == "__main__"):
		start()
