#!/usr/bin/env python3
########################################################################
# Filename    : SenseLED.py
# Description : Controlling an led by infrared Motion sensor.
# Author      : freenove
# modification: 2018/08/03
########################################################################
import RPi.GPIO as GPIO
from time import sleep

ledPin = 12    # define the ledPin
sensorPin = 11    # define the sensorPin

def setup():
	print ('Program is starting...')
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(ledPin, GPIO.OUT)   # Set ledPin's mode is output
	GPIO.setup(sensorPin, GPIO.IN)    # Set sensorPin's mode is input

def irsense_on_callback(channel):
	if GPIO.input(sensorPin)==GPIO.HIGH:
		print('Rise!')
		GPIO.output(ledPin,GPIO.HIGH)
	else:
		print('Fall')
		GPIO.output(ledPin,GPIO.LOW)

def loop():
	GPIO.output(ledPin,GPIO.LOW)
	sleep(5)
	GPIO.add_event_detect(sensorPin, GPIO.BOTH)
	GPIO.add_event_callback(sensorPin, callback=irsense_on_callback)
	sleep(100000)

def destroy():
	GPIO.remove_event_detect(sensorPin)
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
