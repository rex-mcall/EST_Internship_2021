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

# elev motor driver pins
elev_dir_pin    = 21
elev_step_pin   = 20
elev_ms3_pin    = 26
elev_ms2_pin    = 19
elev_ms1_pin    = 13
elev_enable_pin =  6

# az motor driver pins
az_dir_pin    = 24
az_step_pin   = 23
az_ms3_pin    = 22
az_ms2_pin    = 27
az_ms1_pin    = 17
az_enable_pin =  4

# initializing stepper motor pins
GPIO.setmode(GPIO.BCM)

# setup elev motor pins
GPIO.setup(elev_dir_pin, GPIO.OUT)
GPIO.setup(elev_step_pin, GPIO.OUT)
GPIO.setup(elev_ms3_pin, GPIO.OUT)
GPIO.setup(elev_ms2_pin, GPIO.OUT)
GPIO.setup(elev_ms1_pin, GPIO.OUT)
GPIO.setup(elev_enable_pin, GPIO.OUT)

#setup az motor pins
GPIO.setup(az_dir_pin, GPIO.OUT)
GPIO.setup(az_step_pin, GPIO.OUT)
GPIO.setup(az_ms3_pin, GPIO.OUT)
GPIO.setup(az_ms2_pin, GPIO.OUT)
GPIO.setup(az_ms1_pin, GPIO.OUT)
GPIO.setup(az_enable_pin, GPIO.OUT)

# MS1 MS2 MS3 Microstep Resolution Excitation Mode
# L   L   L   Full Step            2 Phase
# H   L   L   Half Step            1-2 Phase
# L   H   L   Quarter Step         W1-2 Phase
# H   H   L   Eighth Step          2W1-2 Phase
# H   H   H   Sixteenth Step       4W1-2 Phase

GPIO.output(elev_ms3_pin, GPIO.LOW)
GPIO.output(elev_ms2_pin, GPIO.HIGH)
GPIO.output(elev_ms1_pin, GPIO.HIGH)
GPIO.output(elev_enable_pin, GPIO.LOW) # Active low to enable motor outputs

GPIO.output(az_ms3_pin, GPIO.LOW)
GPIO.output(az_ms2_pin, GPIO.HIGH)
GPIO.output(az_ms1_pin, GPIO.HIGH)
GPIO.output(az_enable_pin, GPIO.LOW) # Active low to enable motor outputs

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

            matchName = False
            matchElev = False
            matchWait = False
            matchMag  = False

            if self.satName_Search == None:
                matchName = True
            elif re.search(self.satName_Search.lower(), tleLines[0].lower()) != None:
                matchName = True
            else:
                continue

            if self.minElev_Search != None or self.maxWait_Search != None or self.minMag_Search != None:
                satellite = ephem.readtle(tleLines[0], tleLines[1], tleLines[2])
                satellite.compute(observer)
                try:
                    nextPass = observer.next_pass(satellite, singlepass=False)
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

            if self.minMag_Search == None:
                matchMag = True
            elif self.minMag_Search >= satellite.mag:
                matchMag = True
            else:
                continue

            if matchName and matchElev and matchWait and matchMag:
                try:
                    topResults.append(satellite)
                except Exception:
                    satellite = ephem.readtle(tleLines[0], tleLines[1], tleLines[2])
                    satellite.compute(observer)
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

        # initializes variables to remember the current angle of the azimuth and elevation
        self.currStepperAzimuth = 0
        self.currStepperElevation = 0

        # geared down ratios for degrees per step
        self.azDegPerStep = 0.36 / 8 # 1:5 @ 1/4 step
        self.elevDegPerStep = 0.9 / 8# 1:2 at full step

        # amount of time the step pulse is high and low
        self.stepDelay = 0.001

        self.shouldTrack = False
        self.stopThread = False

    def singleStepAltAz(self):
        while not self.stopThread:
            while self.shouldTrack:
                self.shouldHomeMotors = False
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

    # defines how to drive the elevation stepper
    def singleStep_Elev(self, direction):
        GPIO.output(elev_dir_pin, direction)
        GPIO.output(elev_step_pin, GPIO.HIGH)
        sleep(self.stepDelay)
        GPIO.output(elev_step_pin, GPIO.LOW)
        sleep(self.stepDelay)

    #defines how to drive the azimuth stepper
    def singleStep_Az(self, direction):
        GPIO.output(az_dir_pin, direction)
        GPIO.output(az_step_pin, GPIO.HIGH)
        sleep(self.stepDelay)
        GPIO.output(az_step_pin, GPIO.LOW)
        sleep(self.stepDelay)

    def selectSatellite(self, newSatellite):
        self.satellite = newSatellite

    def setShouldTrack(self, trackBool):
        self.shouldTrack = trackBool

    def endThread(self):
        self.stopThread = True

    def cleanupGPIO(self):
        GPIO.cleanup()