import time
import math
import smbus

#importing non-built-in libraries
import GPS
import CMPS12
import FileOps
import Ultrasonic
import MotorServoCtrl


#initialize the bus, compass and servos
GPS.ConnectBus()
CMPS12.ConnectBus()
CMPS12.Calibrated()
MotorServoCtrl.ServoRangeTest()

#Current and goto coordinates and heading variables
currentHeading = 0
gotoHeading    = 0
numofcoords    = 0
obstDistance   = 0
readLats       = []
readLons       = []
currCoord      = [0, 0]
gotoCoord      = [0, 0]
initCoord      = [0, 0]
path = "coordinates.txt"

# Calculate the Goto Heading
def GetGotoHeading():
    
    coordavg0 = 0
    coordavg1 = 0
    
    currCoord = GPS.ReadGPS()
    
    th1 = math.radians(currCoord[0])
    th2 = math.radians(gotoCoord[0])

    delta1 = math.radians(gotoCoord[0] - currCoord[0])
    delta2 = math.radians(gotoCoord[1] - currCoord[1])

    Y = math.sin(delta2)*math.cos(th2)
    X = math.cos(th1)*math.sin(th2) - math.sin(th1)*math.cos(th2)*math.cos(delta2)

    gotoHeading = math.degrees(math.atan2(Y,X))
    gotoHeading = (gotoHeading + 360)%360

    gotoHeading = round(gotoHeading, 1)
    
    return gotoHeading
###

# Set travel Heading While Stationary
def SetHeadingStat(sp):
    currentHeading = CMPS12.Heading()
    while (abs(currentHeading - gotoHeading) > 1.2):
        
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
        
        MotorServoCtrl.Drive(sp)
            
        currentHeading = CMPS12.Heading()

    MotorServoCtrl.Drive(0.1)
    MotorServoCtrl.TurnLeftRight(320)
###
    
# Set Travel Heading While Moving
def SetHeadingMov(sp, hdng):
    currentHeading = CMPS12.Heading()
    while (abs(currentHeading - hdng) > 4):
        
        if(hdng > currentHeading):
            if(abs(hdng - currentHeading) <= 180):
                MotorServoCtrl.TurnLeftRight(270)
            else:
                MotorServoCtrl.TurnLeftRight(370)
        else:
            if(abs(hdng - currentHeading) <= 180):
                MotorServoCtrl.TurnLeftRight(370)
            else:
                MotorServoCtrl.TurnLeftRight(270)
        
        MotorServoCtrl.Drive(sp)     
        currentHeading = CMPS12.Heading()

    MotorServoCtrl.TurnLeftRight(320)

###

# Get the coordinates while stationary
def GetStatCoord(num):
    curCoord = [0, 0]
    coordavg0 = 0
    coordavg1 = 0
    
    for i in range(0, num):
        currCoord = GPS.ReadGPS()
        coordavg0 = coordavg0 + currCoord[0]
        coordavg1 = coordavg1 + currCoord[1]
        CMPS12.delay(10)

    curCoord[0] = round(coordavg0/num, 6)
    curCoord[1] = round(coordavg1/num, 6)
    
    return curCoord
###

##############
#    Main    #
##############

currCoord = GetStatCoord(10)
initCoord = currCoord
currentHeading = CMPS12.Heading()
print("Current Heading = ", currentHeading)
print("Current Coordinates = ", currCoord)
    
'''
inp = float(input("Enter Latitude: "))
gotoCoord[0] = inp
inp = float(input("Enter Longitude: "))
gotoCoord[1] = inp
'''
FileOps.ReadFile(path)
numofcoords = FileOps.ReturnNum()
readLats = FileOps.ReturnLats()
readLons = FileOps.ReturnLons()
readLats.append(currCoord[0])
readLons.append(currCoord[1])
numofcoords = numofcoords + 1

for i in range(0, numofcoords):

    gotoCoord[0] = readLats[i]
    gotoCoord[1] = readLons[i]
    print("Going To: ", gotoCoord)
    gotoHeading = GetGotoHeading()
    print("goto Heading = ", gotoHeading)

    # Setting the car to the Goto Heading twice, for proper allignment
    SetHeadingStat(0.28)
    CMPS12.delay(500)
    currCoord = GetStatCoord(5)
    gotoHeading = GetGotoHeading()
    SetHeadingStat(0.28)
    
    speed = 0.32

    while (speed > 0.1):
        MotorServoCtrl.Drive(speed)
        obstDistance = Ultrasonic.GetDistance()
        currentHeading = CMPS12.Heading()
        currCoord = GPS.ReadGPS()
        gotoHeading = GetGotoHeading()
        SetHeadingMov(speed, gotoHeading)
        
        print("Currently at: ", currCoord)
        
        if((abs(gotoCoord[0] - currCoord[0]) < 0.00001) and (abs(gotoCoord[1] - currCoord[1]) < 0.00001)):
            speed = 0.1
        else:
            speed = 0.32
        
    MotorServoCtrl.Drive(speed)
    print("Destination Reached!")
    
    if (i == numofcoords - 1):
        print("Going to Final Coordinates!")
    else:
        print("Rpceeding to Next Destination in 3 seconds...")
        time.sleep(3)
        
print("Trip Complete!")