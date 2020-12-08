#!/usr/bin/env python3
import socket
import netifaces as ni
import ifaddr
from decimal import *

threshold = 120
delta = 20
certanty = 0.0

HOST = '192.168.50.220'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


def get_ip_ubuntu(hostname):
	ip = ni.ifaddresses(hostname)[ni.AF_INET][0]['addr']
	return ip

def get_ip(hostname):
	adapters = ifaddr.get_adapters()
	for adapter in adapters:
		for ip in adapter.ips:
			ip = ip.ip
			if '192.168.' in ip:
				return ip
	return get_ip_ubuntu(hostname)

def get_ip_raspi():
	hostname = socket.getfqdn()
	(HOST, alias, iplist) = socket.gethostbyname_ex(hostname)
	alias_str = ''.join([i for i in iplist])
	print(hostname + " ip, fqdn: " + HOST + ', ' + alias_str)


def process_data(data, certanty):
	data_s = data.decode("utf-8")
	data_d = Decimal(data_s)
	if data_d < threshold:
		if certanty < 1.0:
			certanty += 1 / delta
	else:
		if certanty > 0.0:
			certanty -= 1/delta
	if certanty > 0.5:
		print("Danger!")
	return certanty

def read_sensor(s):

        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)

        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        print("Waiting for sensor to settle")

        time.sleep(2)

        print("Calculating distance")

        pulse_start_time = 0
        pulse_end_time = 0

        while True:
                GPIO.output(PIN_TRIGGER, GPIO.HIGH)
                time.sleep(0.00001)
                GPIO.output(PIN_TRIGGER, GPIO.LOW)

                while GPIO.input(PIN_ECHO)==0:
                        pulse_start_time = time.time()
                while GPIO.input(PIN_ECHO)==1:
                        pulse_end_time = time.time()

                pulse_duration = pulse_end_time - pulse_start_time
                distance = round(pulse_duration * 17150, 2)
                dist_bytes = str(distance).encode('utf-8')
                print(str(distance))

                time.sleep(0.1)

                send_ack(dist_bytes, s)

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


			certanty = process_data(data, certanty)
			conn.sendall(data)

