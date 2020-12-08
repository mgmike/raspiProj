#!/usr/bin/python3
import time
import socket
import struct
import queue
from threading import Thread

#HOST = '192.168.50.220'	#Desktop
#HOST = '192.168.50.143'	#
#HOST = '127.0.0.1'
HOST = '192.168.50.183'		#RasPiZero1
PORT = 65432

threshold = 120
delta = 20

q = queue.Queue(100)

def get_data(s, q):
	while True:
		data_s = s.recv(1024).decode("utf-8")
		while data_s is None or not data_s:
			data_s = s.recv(1024).decode("utf-8")
		for reading in data_s.split(','):
			if reading:
				q.put(float(reading))


def process_data(q):
	certanty = 0.0
	while True:
		if q.get() < threshold:
			if certanty < 1.0:
				certanty += 1 / delta
		else:
			if certanty > 0.0:
				certanty -= 1 / delta
		if certanty > 0.5:
			print("Danger!")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
error = s.connect((HOST, PORT))
thread_get = Thread(target = get_data, args = (s,q))
thread_process = Thread(target = process_data, args = [q])

while error is OSError:
	error = s.connect((HOST, PORT))
	time.sleep(1)

thread_get.start()
thread_process.start()
