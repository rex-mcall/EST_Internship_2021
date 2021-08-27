import ephem
import datetime as dt
from datetime import datetime, timezone
from math import *
import re

toDeg = 180 / pi
toRad = pi / 180

x = open("/home/pi/Code/EST_Internship_2021/project_code/tleData.txt")
data = x.read().splitlines()
satTLEs = []
currIndex = 0
for line in data:
    if currIndex % 3 == 0:
        currSatTLE = [data[currIndex], data[currIndex + 1], data[currIndex + 2]]
        satTLEs.append(currSatTLE)
    currIndex = currIndex + 1

class satelliteSearch():
    def __init__(self, observer = None, satNameSearch = None, minElevSearch = None, maxWaitSearch = None, beforeVertex = None, minTimeLeft = None, minMag = None):
        self.observer = observer
        self.satName_Search = satNameSearch
        self.minElev_Search = minElevSearch
        self.maxWait_Search = maxWaitSearch
    def getTopResults(self, numResults = 20):
        topResults = []
        for tleLines in satTLEs:
            if len(topResults) >= numResults:
                return topResults

            matchName = False
            matchElev = False
            matchWait = False

            if self.satName_Search == None:
                matchName = True
            elif re.search(self.satName_Search.lower(), tleLines[0].lower()) != None:
                matchName = True
            else:
                continue

            if self.minElev_Search != None or self.maxWait_Search != None:
                satellite = ephem.readtle(tleLines[0], tleLines[1], tleLines[2])
                satellite.compute(self.observer)
                try:
                    nextPass = self.observer.next_pass(satellite, singlepass=False)
                except Exception:
                    continue
                #0  Rise time
                #1  Rise azimuth
                #2  Maximum altitude time
                #3  Maximum altitude
                #4  Set time
                #5  Set azimuth
                riseTime = nextPass[0].datetime()
                riseAz = nextPasss[1] * toDeg
                maxAltTime = nextPass[2].datetime()
                maxAlt = nextPass[3] * toDeg
                setTime = nextPass[4].datetime()
                setAz = nextpass[5] * toDeg

            if self.minElev_Search == None:
                matchElev = True
            elif self.minElev_Search <= maxAlt:
                matchElev = True
            else:
                continue

            if self.maxWait_Search == None:
                matchWait = True
            elif self.maxWait_Search == 0 and (satellite.alt * toDeg) >= 0: # if satellite is currently visible
                matchWait = True
            elif dt.timedelta(minutes=self.maxWait_Search) >= (riseTime - datetime.utcnow()) or satellite.alt * toDeg >= 0:
                matchWait = True
            else:
                continue

            if matchName and matchElev and matchWait:
                satellite = ephem.readtle(tleLines[0], tleLines[1], tleLines[2])
                satellite.compute(self.observer)
                topResults.append(satellite)
            else:
                continue

        return topResults