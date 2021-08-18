from time import sleep
import RPi.GPIO as GPIO
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


x = open("experimental_code/guiTest2/tleData.txt")
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
            if len(topResults) >= 1:
                return topResults
            satellite = ephem.readtle(tleLines[0], tleLines[1], tleLines[2])
            satellite.compute(observer)
            try:
                nextPass = observer.next_pass(satellite, singlepass=False)
            except Exception:
                continue
            riseTime = nextPass[0].datetime()
            maxAlt = nextPass[3] * toDeg
            setTime = nextPass[4].datetime()


            matchName = False
            matchElev = False
            matchWait = False
            matchMag  = False

            if self.satName_Search == None or re.match(self.satName_Search, satellite.name) != None:
                matchName = True
            else:
                continue

            if self.minElev_Search == None or self.minElev_Search <= maxAlt:
                matchElev = True
            else:
                continue

            timeDelta = riseTime - datetime.utcnow()
            if self.maxWait_Search == None or self.maxWait_Search <= timeDelta:
                matchWait = True
            else:
                continue

            if self.minMag_Search == None or self.minMag_Search >= satellite.mag:
                matchMag = True
            else:
                continue

            if matchName and matchElev and matchWait and matchMag:
                topResults.append(satellite)
            else:
                continue

        return topResults

class stepperMotors():
    def __init__(self, satellite=None):
        if satellite == None:
            raise RuntimeError("No satellite parameter passed in")
        else:
            self.satellite = satellite

        observer.date = datetime.now(timezone.utc)
        self.satellite.compute(observer)
        
        self.DIR_Elev_Pin = 20   # Direction GPIO Pin Elevation motor
        self.STEP_Elev_Pin = 21  # Step GPIO Pin Elevation

        self.DIR_Az_Pin = 2 # Direction GPIO Pin Azimuth motor
        self.STEP_Az_Pin = 3 # Step GPIO Pin Azimuth motor

        # initializing stepper motor pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DIR_Elev_Pin, GPIO.OUT)
        GPIO.setup(self.STEP_Elev_Pin, GPIO.OUT)
        GPIO.setup(self.DIR_Az_Pin, GPIO.OUT)
        GPIO.setup(self.STEP_Az_Pin, GPIO.OUT)

        # initializes variables to remember the current angle of the azimuth and elevation
        self.currStepperAzimuth = 0
        self.currStepperElevation = 0

        # geared down ratios for degrees per step
        self.azDegPerStep = 0.36 / 4 # 1:5 @ 1/4 step
        self.elevDegPerStep = 0.9 / 4# 1:2 at full step

        # amount of time the step pulse is high and low
        self.stepDelay = 0.001

        self.shouldTrack = False

    def singleStepAltAz(self):
        while True:
            while self.shouldTrack:
                # refreshes the satellite position with the current time
                observer.date = datetime.now(timezone.utc)
                self.satellite.compute(observer)

                # make sure satellite is above horizon, else reset motors to home position
                if self.satellite.alt * toDeg > 0:

                    # calculates the angle to the correct elevation
                    elevErrDelta = (self.satellite.alt * toDeg) - self.currStepperElevation # <0 motor too high, >0 motor too low

                    # pulses the elevation stepper motor in the correct direction
                    if elevErrDelta >= (self.elevDegPerStep * 3/2):
                        self.singleStep_Elev(0)
                        self.currStepperElevation = self.currStepperElevation + self.elevDegPerStep
                    elif elevErrDelta <= (-self.elevDegPerStep * 3/2):
                        self.singleStep_Elev(1)
                        self.currStepperElevation = self.currStepperElevation - self.elevDegPerStep

                    # determines the most efficient direction to get to the correct azimuth
                    azErrDelta = 0
                    azMotorHomeAngle = self.satellite.az * toDeg
                    if abs((azMotorHomeAngle) - self.currStepperAzimuth) < abs(((azMotorHomeAngle) + 360) - self.currStepperAzimuth) and abs((azMotorHomeAngle) - self.currStepperAzimuth) < abs(((azMotorHomeAngle) - 360) - self.currStepperAzimuth):
                        azErrDelta = (self.satellite.az * toDeg) - self.currStepperAzimuth
                    elif abs(((azMotorHomeAngle) + 360) - self.currStepperAzimuth) < abs(((azMotorHomeAngle) - 360) - self.currStepperAzimuth):
                        azErrDelta = ((self.satellite.az * toDeg) + 360) - self.currStepperAzimuth
                    else:
                        azErrDelta = ((azMotorHomeAngle) - 360) - self.currStepperAzimuth

                    # pulses the azimuth stepper motor in the correct direction
                    if azErrDelta >= (self.azDegPerStep * 3/2):
                        self.singleStep_Az(1)
                        self.currStepperAzimuth = self.currStepperAzimuth + self.azDegPerStep
                    elif azErrDelta <= (-self.azDegPerStep * 3/2) :
                        self.singleStep_Az(0)
                        self.currStepperAzimuth = self.currStepperAzimuth - self.azDegPerStep
                # reset motors to home position
                else:
                    # calculates the angle to the correct elevation
                    elevMotorHomeAngle = 0
                    elevErrDelta = elevMotorHomeAngle - self.currStepperElevation # <0 motor too high, >0 motor too low

                    # pulses the elevation stepper motor in the correct direction
                    if elevErrDelta >= (self.elevDegPerStep * 3/2):
                        self.singleStep_Elev(0)
                        self.currStepperElevation = self.currStepperElevation + self.elevDegPerStep
                    elif elevErrDelta <= (-self.elevDegPerStep * 3/2):
                        self.singleStep_Elev(1)
                        self.currStepperElevation = self.currStepperElevation - self.elevDegPerStep

                    # determines the most efficient direction to get to the correct azimuth
                    azErrDelta = 0
                    azMotorHomeAngle = 0
                    if abs((azMotorHomeAngle) - self.currStepperAzimuth) < abs(((azMotorHomeAngle) + 360) - self.currStepperAzimuth) and abs((azMotorHomeAngle) - self.currStepperAzimuth) < abs(((azMotorHomeAngle) - 360) - self.currStepperAzimuth):
                        azErrDelta = (self.satellite.az * toDeg) - self.currStepperAzimuth
                    elif abs(((azMotorHomeAngle) + 360) - self.currStepperAzimuth) < abs(((azMotorHomeAngle) - 360) - self.currStepperAzimuth):
                        azErrDelta = ((self.satellite.az * toDeg) + 360) - self.currStepperAzimuth
                    else:
                        azErrDelta = ((azMotorHomeAngle) - 360) - self.currStepperAzimuth

                    # pulses the azimuth stepper motor in the correct direction
                    if azErrDelta >= (self.azDegPerStep * 3/2):
                        self.singleStep_Az(1)
                        self.currStepperAzimuth = self.currStepperAzimuth + self.azDegPerStep
                    elif azErrDelta <= (-self.azDegPerStep * 3/2) :
                        self.singleStep_Az(0)
                        self.currStepperAzimuth = self.currStepperAzimuth - self.azDegPerStep
                    
                    if azErrDelta < 1 and elevErrDelta < 1:
                        self.shouldTrack=False

    # defines how to drive the elevation stepper
    def singleStep_Elev(self, direction):
        GPIO.output(self.DIR_Elev_Pin, direction)
        GPIO.output(self.STEP_Elev_Pin, GPIO.HIGH)
        sleep(self.stepDelay)
        GPIO.output(self.STEP_Elev_Pin, GPIO.LOW)
        sleep(self.stepDelay)

    #defines how to drive the azimuth stepper
    def singleStep_Az(self, direction):
        GPIO.output(self.DIR_Az_Pin, direction)
        GPIO.output(self.STEP_Az_Pin, GPIO.HIGH)
        sleep(self.stepDelay)
        GPIO.output(self.STEP_Az_Pin, GPIO.LOW)
        sleep(self.stepDelay)

    def selectSatellite(self, newSatellite):
        self.satellite = newSatellite

    def setShouldTrack(self, trackBool):
        self.shouldTrack = trackBool

    def cleanupGPIO():
        GPIO.cleanup()