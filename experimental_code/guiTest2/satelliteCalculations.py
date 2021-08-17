import ephem
import datetime as dt
from datetime import datetime, timezone
from math import *
import re

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


x = open("experimental_code\\guiTest2\\tleData.txt")
data = x.read().splitlines()
satTLEs = []
currIndex = 0
for line in data:
    if currIndex % 3 == 0:
        currSatTLE = [data[currIndex], data[currIndex + 1], data[currIndex + 2]]
        satTLEs.append(currSatTLE)
    currIndex = currIndex + 1

class satelliteSearch():
    def __init__(self, satNameSearch = None, minElevSearch = None, maxWaitSearch = None, minMagSearch = None):
        self.satName_Search = satNameSearch
        self.minElev_Search = minElevSearch
        self.maxWait_Search = maxWaitSearch
        self.minMag_Search = minMagSearch
    def getTop5Results(self):
        topResults = []
        for tleLines in satTLEs:
            if len(topResults) >= 5:
                return topResults
            satellite = ephem.readtle(tleLines[0], tleLines[1], tleLines[2])
            satellite.compute(observer)
            try:
                nextPass = observer.next_pass(satellite, singlepass=False)
            except Exception:
                continue
            riseTime = nextPass[0].datetime()
            riseAzimuth = nextPass[1] * toDeg
            maxAltTime = nextPass[2].datetime()
            maxAlt = nextPass[3] * toDeg
            setTime = nextPass[4].datetime()
            setAzimuth = nextPass[5] * toDeg

            matchName = False
            matchElev = False
            matchWait = False
            matchMag  = False

            if self.satName_Search == None or re.match(self.satName_Search, satellite.name) != None:
                matchName = True

            if self.minElev_Search == None or self.minElev_Search <= maxAlt:
                matchElev = True

            timeDelta = riseTime - datetime.utcnow()
            if self.maxWait_Search == None or self.maxWait_Search <= timeDelta:
                matchWait = True

            if self.minMag_Search == None or self.minMag_Search >= satellite.mag:
                matchMag = True

            if matchName and matchElev and matchWait and matchMag:
                topResults.append(satellite)

        return topResults