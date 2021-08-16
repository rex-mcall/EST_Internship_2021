

import ephem
import datetime as dt
from datetime import datetime, timezone
from math import *

# calculated constants to convert to and from radians
toDeg = 180 / pi
toRad = pi / 180

# annapolis, md lat/long
latitude = 38.9784
longitude = -76.4922

# sets up reveiver locaiton
observer = ephem.Observer()
#convert to Angle type by multiplying ephem.degree
observer.lat = latitude * ephem.degree
observer.lon = longitude * ephem.degree
observer.elev = 13
observer.date = datetime.now(timezone.utc)

x = open("experimental_code\\largeTLEData\\tleData.txt")
data = x.read().splitlines()
satTLEs = []
currIndex = 0
for line in data:
    if currIndex % 3 == 0:
        currSatTLE = [data[currIndex], data[currIndex + 1], data[currIndex + 2]]
        satTLEs.append(currSatTLE)
    currIndex = currIndex + 1

currentlyVisibleSats = []
soonVisibleSats = []

for tleLines in satTLEs:
    satellite = ephem.readtle(tleLines[0], tleLines[1], tleLines[2])
    satellite.compute(observer)

    nextPass = observer.next_pass(satellite, singlepass=False)
    riseTime = nextPass[0].datetime()
    riseAzimuth = nextPass[1] * toDeg
    maxAltTime = nextPass[2].datetime()
    maxAlt = nextPass[3] * toDeg
    setTime = nextPass[4].datetime()
    setAzimuth = nextPass[5] * toDeg

    currentlyVisible = False
    soonVisible = False
    if datetime.utcnow() < riseTime and riseTime > setTime: # current time is less than the next rise and setTime hasn't occured yet
        currentlyVisible = True
    elif 



print(x)