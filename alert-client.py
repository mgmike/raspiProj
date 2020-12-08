#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import socket
import struct

HOST = '192.168.50.220'
#HOST = '192.168.50.143'
#HOST = '127.0.0.1'
PORT = 65432
PIN_TRIGGER = 7
PIN_ECHO = 11


def send_ack(dist_bytes, s):
	s.sendall(dist_bytes)
	data = s.recv(1024)
	print('Received', repr(data))


def process_data(data, certanty):
	data_s = data.decode("utf-8")
	data_d = Decimal(data_s)
	if data_d < threshold:
		if certanty < 1.0:
			certanty += 1 / delta
	else:
		if certanty > 0.0:
			certanty -= 1 / delta
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

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	error = s.connect((HOST, PORT))

	while error is OSError:
		error = s.connect((HOST, PORT))
		time.sleep(1)

	read_sensor(s)

finally:
	GPIO.cleanup()
	print("done!")
