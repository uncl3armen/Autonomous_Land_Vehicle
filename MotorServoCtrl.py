from __future__ import division
import time
import Adafruit_PCA9685
from adafruit_servokit import ServoKit

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

pwm.set_pwm_freq(60)
kit = ServoKit(channels=8)

def TurnLeftRight(pos):
    pwm.set_pwm(15, 0, pos)
    time.sleep(0.1)
    
def Drive(throttle):
    kit.continuous_servo[1].throttle = throttle
    time.sleep(0.1)
    
def ServoCenter():
    TurnLeftRight(320)

def ServoRangeTest():
    TurnLeftRight(420)
    time.sleep(1)
    TurnLeftRight(220)
    time.sleep(1)
    ServoCenter()
    time.sleep(1)
    Drive(0.15)
    time.sleep(0.2)
    Drive(0.1)
    
    print("Servo and Motor OK!")

    

    #420 left max
    #320 center
    #220 right max
    
    #Speed is between 0.1 and 1
    #less than 0.1 is reverse
    
    #0.1 is stop
    #0.30-0.35 is decent forward motion for testing
