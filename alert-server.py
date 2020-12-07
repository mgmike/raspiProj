#!/usr/bin/env python3
import socket
import netifaces as ni

HOST = '192.168.50.220'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def get_ip(hostname):
	ip = ni.ifaddresses(hostname)[ni.AF_INET][0]['addr']
	return ip

def get_ip_raspi():
	hostname = socket.getfqdn()
	(HOST, alias, iplist) = socket.gethostbyname_ex(hostname)
	alias_str = ''.join([i for i in iplist])
	print(hostname + " ip, fqdn: " + HOST + ', ' + alias_str)

HOST = get_ip('wifi0')
print(HOST)

#except:
#	HOST = socket.gethostbyname(socket.gethostname())
#	print("Host ip: " + HOST)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
while True:
	s.listen()
	conn, addr = s.accept()
	with conn:
		print('Connected by', addr)
		while True:
			data = conn.recv(1024)
			if not data:
				break
			print(data)
			conn.sendall(data)

