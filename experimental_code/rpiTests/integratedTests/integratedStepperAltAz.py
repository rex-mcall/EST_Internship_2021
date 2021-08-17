from time import sleep
import RPi.GPIO as GPIO

import ephem
import datetime as dt
from datetime import datetime, timezone
from math import *

# calculated constants to convert to and from radians
toDeg = 180 / pi
toRad = pi / 180


#tle of the current satellite to track
tle_string = """
STARLINK-2736           
1 48640U 21044C   21224.58334491 -.00006554  00000-0 -42144-3 0  9991
2 48640  53.0533  54.0006 0001698 107.2301 200.8002 15.06403949  3596
"""

# parse tle data and initialize satellite as an EarthSatellite object
tle_lines = tle_string.strip().splitlines()
satellite = ephem.readtle(tle_lines[0], tle_lines[1], tle_lines[2])

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

DIR_Elev_Pin = 20   # Direction GPIO Pin Elevation motor
STEP_Elev_Pin = 21  # Step GPIO Pin Elevation

DIR_Az_Pin = 2 # Direction GPIO Pin Azimuth motor
STEP_Az_Pin = 3 # Step GPIO Pin Azimuth motor


# initializing stepper motor pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_Elev_Pin, GPIO.OUT)
GPIO.setup(STEP_Elev_Pin, GPIO.OUT)
GPIO.setup(DIR_Az_Pin, GPIO.OUT)
GPIO.setup(STEP_Az_Pin, GPIO.OUT)

# initializes variables to remember the current angle of the azimuth and elevation
currStepperAzimuth = 0
currStepperElevation = 0

# geared down ratios for degrees per step
azDegPerStep = 0.36 / 4 # 1:5 @ 1/4 step
elevDegPerStep = 0.9 / 4# 1:2 at full step

# amount of time the step pulse is high and low
stepDelay = 0.001

# defines how to drive the elevation stepper
def singleStep_Elev(direction):
    GPIO.output(DIR_Elev_Pin, direction)
    GPIO.output(STEP_Elev_Pin, GPIO.HIGH)
    sleep(stepDelay)
    GPIO.output(STEP_Elev_Pin, GPIO.LOW)
    sleep(stepDelay)

#defines how to drive the azimuth stepper
def singleStep_Az(direction):
    GPIO.output(DIR_Az_Pin, direction)
    GPIO.output(STEP_Az_Pin, GPIO.HIGH)
    sleep(stepDelay)
    GPIO.output(STEP_Az_Pin, GPIO.LOW)
    sleep(stepDelay)

# gathers data before checking if the satellite is currently visible
satellite.compute(observer)
nextPass = observer.next_pass(satellite, singlepass=False)
riseTime = nextPass[0].datetime()
riseAzimuth = nextPass[1] * toDeg
maxAltTime = nextPass[2].datetime()
maxAlt = nextPass[3] * toDeg
setTime = nextPass[4].datetime()
setAzimuth = nextPass[5] * toDeg


# checks to see if the satellite is currently in the sky 
# if sat is not in sky, inform the user of how long until the satellite is in the sky
if datetime.utcnow() < riseTime and riseTime < setTime:
    timeTillRise = riseTime - datetime.utcnow()
    secondsToWait = timeTillRise.total_seconds()
    print("Waiting ", secondsToWait / 60 , " minutes till satellite rise.")
    sleep(secondsToWait + 5)

# sets up the satellite data
observer.date = datetime.now(timezone.utc)
satellite.compute(observer)

# temp var for print statements
currIteration = 0

while (satellite.alt * toDeg) >= 0 :
    # refreshes the satellite position with the current time
    observer.date = datetime.now(timezone.utc)
    satellite.compute(observer)
    if currIteration % 1000 == 0:
        print("azimuth = ", satellite.az, " --- stepper position az = ", currStepperAzimuth)
        print("elev = ", satellite.alt, " --- stepper position elev = ", currStepperElevation)
        print("- - - - - - - - - - - - - - - ")
    currIteration = currIteration + 1

    # calculates the angle to the correct elevation
    elevErrDelta = (satellite.alt * toDeg) - currStepperElevation # <0 motor too high, >0 motor too low

    # pulses the elevation stepper motor in the correct direction
    if elevErrDelta >= (elevDegPerStep * 3/2):
        singleStep_Elev(0)
        currStepperElevation = currStepperElevation + elevDegPerStep
    elif elevErrDelta <= (-elevDegPerStep * 3/2):
        singleStep_Elev(1)
        currStepperElevation = currStepperElevation - elevDegPerStep

    # determines the most efficient direction to get to the correct azimuth
    azErrDelta = 0
    currSatAzDeg = satellite.az * toDeg
    if abs((currSatAzDeg) - currStepperAzimuth) < abs(((currSatAzDeg) + 360) - currStepperAzimuth) and abs((currSatAzDeg) - currStepperAzimuth) < abs(((currSatAzDeg) - 360) - currStepperAzimuth):
        azErrDelta = (satellite.az * toDeg) - currStepperAzimuth
    elif abs(((currSatAzDeg) + 360) - currStepperAzimuth) < abs(((currSatAzDeg) - 360) - currStepperAzimuth):
        azErrDelta = ((satellite.az * toDeg) + 360) - currStepperAzimuth
    else:
        azErrDelta = ((currSatAzDeg) - 360) - currStepperAzimuth

    # pulses the azimuth stepper motor in the correct direction
    if azErrDelta >= (azDegPerStep * 3/2):
        singleStep_Az(1)
        currStepperAzimuth = currStepperAzimuth + azDegPerStep
    elif azErrDelta <= (-azDegPerStep * 3/2) :
        singleStep_Az(0)
        currStepperAzimuth = currStepperAzimuth - azDegPerStep

# release GPIO pins back to the Pi
GPIO.cleanup()