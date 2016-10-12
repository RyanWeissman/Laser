#!/usr/bin/python
import time
import RPi.GPIO as GPIO
import pygame
from sys import stdout

GPIO.setmode(GPIO.BOARD)

def airhorn():
    pygame.mixer.init()
    pygame.mixer.music.load("airhorn.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    

def rc_time(rc_pin):
    reading = 0
    GPIO.setup(rc_pin, GPIO.OUT)
    GPIO.output(rc_pin, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(rc_pin, GPIO.IN)
    while GPIO.input(rc_pin) == GPIO.LOW:
        reading += 1
    return reading


def experiment():
    while True:
        print rc_time(11)
    

def calibrate(duraiton):
    print "Beginning Calibration..."
    time_e = time.time() + duraiton  # end time is duration seconds past present
    min_v = rc_time(11)
    max_v = rc_time(11)
    while time.time() < time_e:
        t = rc_time(11)
        if t < min_v:
            min_v = t
        if t > max_v:
            max_v = t
    print "Calibration finished!"
    print "Min: %d" % min_v
    print "Max: %d" % max_v
    return min_v, max_v


def run_game(off, on):
    if on[0] <= rc_time(11) <= on[1]:
        print "Your game has started."
    time_s = time.time()
    time_f = 0
    light_is_on = True
    while light_is_on:
        light_level = rc_time(11)
        print "light level is %d" % light_level
        if off[0] <= light_level <= off[1]:
            light_is_on = False
            time_f = time.time()
            airhorn()
            print "You lose, please be more careful next time..."
    print "Your time was %f seconds." % (time_f - time_s)
    again = raw_input("Would you like to play again with the same calibration? (Y/N)")
    if again == "Y" or again == "y" or again == "yes":
        run_game(off, on)


# begin game code
print "Welcome to laser maze version 0.2"

dur = 10
try:
    dur = int(raw_input("Enter calibration time in seconds: "))
except ValueError:
    print "Not a number"

print "Calibrating OFF light levels in "
for count in range(5, 0, -1):
    stdout.write("\r%d" % count)
    stdout.flush()
    time.sleep(1)
stdout.write("\n")

off_v = calibrate(dur)

print "Calibrating ON light levels in "
for count in range(5, 0, -1):
    stdout.write("\r%d" % count)
    stdout.flush()
    time.sleep(1)
stdout.write("\n")

on_v = calibrate(dur)

print "Make sure the laser is ON when the game starts!"
print "Your game will begin in "
for count in range(10, 0, -1):
    stdout.write("\r%d" % count)
    stdout.flush()
    time.sleep(1)
stdout.write("\n")

run_game(off_v, on_v)
