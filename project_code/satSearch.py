import ephem
import datetime as dt
from datetime import datetime, timezone
from math import *
import re

toDeg = 180 / pi
toRad = pi / 180

# open tle text file
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
    def __init__(self, observer = None, satNameSearch = None, minElevSearch = None, minCurrElevSearch = None, maxWaitSearch = None, beforeVertex = None, minTimeLeft = None, minMag = None):
        self.observer = observer
        self.satName_Search = satNameSearch          # matches text to satellite name w/ regex
        self.minElev_Search = minElevSearch          # minimum vertex elevation, in degrees
        self.minCurrElev_Search = minCurrElevSearch  # minimum current elevation, in degrees
        self.maxWait_Search = maxWaitSearch          # max wait till satellite rises, in mins (0=currently up)
        self.beforeVertex = beforeVertex             # satellite can't have passed vertex yet
        self.minTimeLeft = minTimeLeft               # min time left visible
        self.minMag = minMag                         # min magnitude of the satellite
    def getTopResults(self, numResults = 5):
        topResults = []
        for tleLines in satTLEs:
            # return array of sats if enough hits are found
            if len(topResults) >= numResults:
                return topResults

            matchName         = False   # matches text to satellite name w/ regex
            matchElev         = False   # minimum vertex elevation, in degrees
            matchCurrElev     = False   # minimum current elevation, in degrees
            matchWait         = False   # max wait till satellite rises, in mins (0=currently up)
            matchBfVtx        = False   # satellite can't have passed vertex yet
            matchMinTimeLeft  = True    # min time left visible
            matchMinMag       = True    # min magnitude of the satellite

            # tests to see if sat name matches query
            if self.satName_Search == None:
                matchName = True
            elif re.search(self.satName_Search.lower(), tleLines[0].lower()) != None:
                matchName = True
            else:
                continue

            # precomputes satellite orbit only when necessary
            if self.minElev_Search != None or self.minCurrElev_Search != None or self.maxWait_Search != None or self.beforeVertex != None or self.minTimeLeft != None:
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
                riseTime   = nextPass[0].datetime()
                riseAz     = nextPass[1] * toDeg
                maxAltTime = nextPass[2].datetime()
                maxAlt     = nextPass[3] * toDeg
                setTime    = nextPass[4].datetime()
                setAz      = nextPass[5] * toDeg

            # tests for vertex elevation
            if self.minElev_Search == None:
                matchElev = True
            elif self.minElev_Search <= maxAlt:
                matchElev = True
            else:
                continue

            # tests for current satellite elevation
            if self.minCurrElev_Search == None:
                matchCurrElev = True
            elif self.minCurrElev_Search <= satellite.alt * toDeg:
                matchCurrElev = True
            else:
                continue

            # tests for wait till rise time
            if self.maxWait_Search == None:
                matchWait = True
            elif self.maxWait_Search == 0 and (satellite.alt * toDeg) >= 0: # if satellite is currently visible
                matchWait = True
            elif dt.timedelta(minutes=self.maxWait_Search) >= (riseTime - datetime.utcnow()) or satellite.alt * toDeg >= 0:
                matchWait = True
            else:
                continue

            # tests to see if sat has already passed vertex elev
            if self.beforeVertex == None:
                matchBfVtx = True
            elif self.beforeVertex == 1 and maxAltTime > datetime.utcnow():
                matchBfVtx = True
            else:
                continue

            # valid result if sat matches all search criteria
            if matchName and matchElev and matchCurrElev and matchWait and matchBfVtx and matchMinTimeLeft and matchMinMag:
                satellite = ephem.readtle(tleLines[0], tleLines[1], tleLines[2])
                satellite.compute(self.observer)
                topResults.append(satellite)
            else:
                continue

        return topResults
