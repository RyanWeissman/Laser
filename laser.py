#!/usr/bin/python
import time
import RPi.GPIO as GPIO
import vlc

GPIO.setmode(GPIO.BOARD)

def RCtime (RCpin):
	reading = 0
	GPIO.setup(RCpin, GPIO.OUT)
	GPIO.output(RCpin, GPIO.LOW)
	time.sleep(0.1)
	
	GPIO.setup(RCpin, GPIO.IN)
	while (GPIO.input(RCpin) == GPIO.LOW):
		reading += 1
	return reading

def CheckLight():
        while True:
                t = RCtime(11)
                print RCtime(11)

CheckLight()

def Calibrate():
        endTime = time.time() + 20 # end time is 20s past present
        minLight = RCtime(11)
        while time.time() < endTime:
                t = RCtime(11)
