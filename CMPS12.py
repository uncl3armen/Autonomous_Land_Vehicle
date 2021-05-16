import time
import math
import smbus

i2c_Bus_num   = 1

Chip_Address  = 0x60     # Compass i2c address

MSB_Reg = 0x02           # MSB
LSB_Reg = 0x03           # LSB
Cal_reg = 0x1E           # Calibration Register returns 8 bits
                         # Each group of two represents calibration status
                         # 11 = fully calibrated
Cmd_reg = 0x00           # Command Register
   
declination   = 11.766667


# Connect to i2c bus
def ConnectBus():
    global bus
    bus = smbus.SMBus(i2c_Bus_num)

# N-milisecond delay function
def delay(tme):
    time.sleep(tme/1000)


########## i2c Functions ##########
    
def i2cRead(addr):
    data = bus.read_byte_data(Chip_Address, addr)
    return data

def i2cWrite_no_reg(dat):    
    bus.write_byte(Chip_Address, dat)
    
def i2cWrite(addr, dat):    
    bus.write_byte_data(Chip_Address, addr, dat)

############


# Read Calibration status
def Calibrated():
    cal = bin(i2cRead(0x1E))
    
    if(cal == "0b11111111"):
        print("All Modules Calibrated!")
    else:
        print("Recalibration Required!")
        print("Error Code: ", cal)
    return cal

# Store Calibrated Profile
def StoreCalProfile():
    print("Updating Calibration Profile...")
    print("0%")
    delay(50)
    
    i2cWrite(0x00, 0xF0)
    delay(20)
    print("33%...")
    i2cWrite(0x00, 0xF5)
    delay(20)
    print("67%...")
    i2cWrite(0x00, 0xF6)
    delay(20)
    
    print("100%...")
    print("Calibration Profile Updated!")

# Erase stored profile
def EraseCalProfile():
    print("Erasing Calibration Profile...")
    print("0%")
    delay(50)
    
    i2cWrite(0x00, 0xE0)
    delay(20)
    print("33%...")
    i2cWrite(0x00, 0xE5)
    delay(20)
    print("67%...")
    i2cWrite(0x00, 0xE2)
    delay(20)
    
    print("100%...")
    print("Calibration Profile Erased!")

# Heading
def Heading():
    MSB = i2cRead(MSB_Reg)
    LSB = i2cRead(LSB_Reg)
    
    data = (MSB << 8) | LSB
    
    heading = round((data/10 - 180 + declination), 1)
    
    if(heading < 0):
        heading = heading + 360
    
    return heading


#ConnectBus()
#StoreCalProfile()