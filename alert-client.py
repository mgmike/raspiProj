#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import socket

HOST = '192.168.50.220'
#HOST = '127.0.0.1'
PORT = 65432


try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))

	GPIO.setmode(GPIO.BOARD)
	PIN_TRIGGER = 7
	PIN_ECHO = 11

	GPIO.setup(PIN_TRIGGER, GPIO.OUT)
	GPIO.setup(PIN_ECHO, GPIO.IN)

	GPIO.output(PIN_TRIGGER, GPIO.LOW)

	print("Waiting for sensor to settle")

	time.sleep(2)

	print("Calculating distance")

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
		dist_str = "Signal: " + str(distance) 
		dist_bytes = dist_str.encode('utf-8')
		print(dist_str)

		time.sleep(0.3)

		if distance < 130:
			s.sendall(dist_bytes)
			data = s.recv(1024)
			print('Received', repr(data))

finally:
	GPIO.cleanup()
