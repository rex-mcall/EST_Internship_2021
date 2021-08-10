from time import sleep
import RPi.GPIO as GPIO

import ephem
import datetime as dt
from datetime import datetime, timezone
from math import *
toDeg = 180 / pi
toRad = pi / 180

tle_string = """
STARLINK-1289           
1 45102U 20006BL  21222.32244386  .00000333  00000-0  41274-4 0  9992
2 45102  53.0541 194.1758 0001205  49.3216 310.7877 15.06392063 84954
"""

tle_lines = tle_string.strip().splitlines()
satellite = ephem.readtle(tle_lines[0], tle_lines[1], tle_lines[2])

latitude = 38.9784
longitude = -76.4922

observer = ephem.Observer()
#convert to Angle type by multiplying ephem.degree
observer.lat = latitude * ephem.degree
observer.lon = longitude * ephem.degree
observer.elev = 13
observer.date = datetime.now(timezone.utc)

DIR_Elev_Pin = 20   # Direction GPIO Pin
STEP_Elev_Pin = 21  # Step GPIO Pin
elevDegPerStep = 0.9

DIR_Az_Pin = 2
STEP_Az_Pin = 3
azDegPerStep = 0.36

GPIO.setmode(GPIO.BCM)

GPIO.setup(DIR_Elev_Pin, GPIO.OUT)
GPIO.setup(STEP_Elev_Pin, GPIO.OUT)

GPIO.setup(DIR_Az_Pin, GPIO.OUT)
GPIO.setup(STEP_Az_Pin, GPIO.OUT)

currXAngle = 0
currYAngle = 0

stepDelay = 0.01

def singleStep_Elev(direction):
    GPIO.output(DIR_Elev_Pin, direction)
    GPIO.output(STEP_Elev_Pin, GPIO.HIGH)
    sleep(stepDelay)
    GPIO.output(STEP_Elev_Pin, GPIO.LOW)
    sleep(stepDelay)

def singleStep_Az(direction):
    GPIO.output(DIR_Az_Pin, direction)
    GPIO.output(STEP_Az_Pin, GPIO.HIGH)
    sleep(stepDelay)
    GPIO.output(STEP_Az_Pin, GPIO.LOW)
    sleep(stepDelay)

satellite.compute(observer)
nextPass = observer.next_pass(satellite, singlepass=False)
riseTime = nextPass[0].datetime()
riseAzimuth = nextPass[1] * toDeg
maxAltTime = nextPass[2].datetime()
setAzimuth = nextPass[5] * toDeg
setTime = nextPass[4].datetime()



if datetime.utcnow() < riseTime and riseTime < setTime:
    timeTillRise = riseTime - datetime.utcnow()
    secondsToWait = timeTillRise.total_seconds()
    print("Waiting ", secondsToWait / 60 , " minutes till satellite rise.")
    sleep(secondsToWait + 5)

observer.date = datetime.now(timezone.utc)
satellite.compute(observer)

while (satellite.alt * toDeg) >= 0 :
    observer.date = datetime.now(timezone.utc)
    satellite.compute(observer)

    elevErrDelta = (satellite.alt * toDeg) - currYAngle # <0 motor too high, >0 motor too low

    if elevErrDelta > 0 and elevErrDelta <= (elevDegPerStep * 3/2):
        print("ystep+")
        singleStep_Elev(1)
        currYAngle = currYAngle + elevDegPerStep
    elif elevErrDelta <= 0 and elevErrDelta >= (elevDegPerStep * 3/2):
        print("ystep-")
        singleStep_Elev(0)
        currYAngle = currYAngle - elevDegPerStep

    # if (currXAngle % 360) < (satellite.az * toDeg) + ((azDegPerStep + 0.1)) :
    #     singleStep_Az(1)
    #     currXAngle = currXAngle + azDegPerStep
    # elif (currXAngle % 360) >= (satellite.az * toDeg) - ((azDegPerStep + 0.1)) :
    #     singleStep_Az(0)
    #     currXAngle = currXAngle - azDegPerStep
GPIO.cleanup()