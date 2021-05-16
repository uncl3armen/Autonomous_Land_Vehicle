lats = []
lons = []
numofCoord = 0

# Read the Contents of the File
def ReadFile(path):
    file = open(path, "r")
    data = ""
    text = file.readlines()
    global numofCoord

    for data in text:
        lat,lon = data.strip().split(',')
        lats.append(float(lat))
        lons.append(float(lon))
        numofCoord = numofCoord + 1

    file.close()
###
    
# Return the array of Latitudes
def ReturnLats():
    return lats
###

# Return the array of Latitudes
def ReturnLons():
    return lons
###

# Return the array of Latitudes
def ReturnNum():
    return numofCoord
###
