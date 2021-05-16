import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

sensorTrigger = 18
sensorEcho    = 24

GPIO.setwarnings(False)
GPIO.setup(sensorTrigger, GPIO.OUT)
GPIO.setup(sensorEcho, GPIO.IN)

def GetDistance():
    GPIO.output(sensorTrigger, True)
    time.sleep(0.00001)
    GPIO.output(sensorTrigger, False)
    
    startTime = time.time()
    stopTime  = time.time()
    
    while (GPIO.input(sensorEcho) == 0):
        startTime = time.time()
        
    while (GPIO.input(sensorEcho) == 1):
        stopTime = time.time()
    
    totalTime = stopTime - startTime
    distance = round(totalTime*17150, 1)
    
    return distance

'''
while True:
    d = round(GetDistance(), 2)
    print("Distance = ", d)
    time.sleep(1)
'''