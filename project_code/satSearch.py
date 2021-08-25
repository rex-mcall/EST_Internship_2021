import ephem
import datetime as dt
from datetime import datetime, timezone
from math import *
import re



x = open("tleData.txt")
data = x.read().splitlines()
satTLEs = []
currIndex = 0
for line in data:
    if currIndex % 3 == 0:
        currSatTLE = [data[currIndex], data[currIndex + 1], data[currIndex + 2]]
        satTLEs.append(currSatTLE)
    currIndex = currIndex + 1

class satelliteSearch():
    def __init__(self, observer = None, satNameSearch = None, minElevSearch = None, maxWaitSearch = None):
        self.observer = observer
        self.satName_Search = satNameSearch
        self.minElev_Search = minElevSearch
        self.maxWait_Search = maxWaitSearch
    def getTopResults(self, numResults = 5):
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
                riseTime = nextPass[0].datetime()
                maxAlt = nextPass[3] * toDeg
                setTime = nextPass[4].datetime()

            if self.minElev_Search == None:
                matchElev = True
            elif self.minElev_Search <= maxAlt:
                matchElev = True
            else:
                continue

            if self.maxWait_Search == None:
                matchWait = True
            elif self.maxWait_Search == dt.timedelta(minutes=0) and satellite.alt * toDeg >= 0: # if satellite is currently visible
                matchWait = True
            elif self.maxWait_Search <= riseTime - datetime.utcnow() or satellite.alt * toDeg >= 0:
                matchWait = True
            else:
                continue

            if matchName and matchElev and matchWait:
                try:
                    topResults.append(satellite)
                except Exception:
                    satellite = ephem.readtle(tleLines[0], tleLines[1], tleLines[2])
                    satellite.compute(self.observer)
                    topResults.append(satellite)
            else:
                continue

        return topResults