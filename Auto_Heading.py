import time
import math
import smbus
import CMPS12
import MotorServoCtrl


CMPS12.ConnectBus()
CMPS12.Calibrated()
MotorServoCtrl.ServoRangeTest()

gotoHeading = 0

currentHeading = CMPS12.Heading()
print("Heading = ", currentHeading)

inp = float(input("Enter Heading: "))
gotoHeading = inp

while (abs(currentHeading - gotoHeading) >5):
    
    
    if(gotoHeading > currentHeading):
        if(abs(gotoHeading - currentHeading) <= 180):
            MotorServoCtrl.TurnLeftRight(220)
        else:
            MotorServoCtrl.TurnLeftRight(420)
    else:
        if(abs(gotoHeading - currentHeading) <= 180):
            MotorServoCtrl.TurnLeftRight(420)
        else:
            MotorServoCtrl.TurnLeftRight(220)
    
    MotorServoCtrl.Drive(0.30)
        
    currentHeading = CMPS12.Heading()
    print("Heading = ", currentHeading)

MotorServoCtrl.Drive(0.1)
MotorServoCtrl.TurnLeftRight(320)

print("We Have Arrived!")