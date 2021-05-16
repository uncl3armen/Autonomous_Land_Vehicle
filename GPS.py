import time
import json
import smbus
import logging

BUS = None
address = 0x42
gpsReadInterval = 0.1
LOG = logging.getLogger()

# Connect the Bus
def ConnectBus():
    global BUS
    BUS = smbus.SMBus(1)
#

# Read GPS Coordinates
def ReadGPS():
    
    gps = [-1000.0,-1000.0]
    
    while(gps[0] == -1000):
        
        c = None
        response = []
        lat = ""
        lon = ""
        
        try:
            while c!=10: # Newline, or bad char.
                c = BUS.read_byte(address)
                if c != 255:
                    response.append(c) 
                                                     
            gpsChars = ''.join(chr(c) for c in response)
            
            if(gpsChars.startswith("$GNGGA")):
                lat, unusd ,lon, drctn = gpsChars.strip().split(',')[2:6]
            elif(gpsChars.startswith("$GNGLL")):
                lat, unusd ,lon, drctn = gpsChars.strip().split(',')[1:5]
                
            try:
                lat = float(lat)
                lon = float(lon)
                
                latitude_deg = int((float(lat)/100))
                latitude_min = float(lat) - (latitude_deg*100)
                latitude = round((latitude_deg + (latitude_min/60)), 6)
                
                longitude_deg = int((float(lon)/100))
                longitude_min = float(lon) - (longitude_deg*100)
                longitude = round((longitude_deg + (longitude_min/60)), 6)
                if(drctn == 'W'):
                    longitude = (-1)*longitude
        
                gps[0] = latitude
                gps[1] = longitude
            except Exception as e:
                pass
        
        except IOError:
            time.sleep(0.5)
            ConnectBus()
        except Exception as e:
            print(e)
            LOG.error(e)
            
    return gps
'''   
ConnectBus()
while True:
    test = ReadGPS()
    print("Coord = ", test)
'''