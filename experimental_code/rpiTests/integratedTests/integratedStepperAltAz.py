from time import sleep
import RPi.GPIO as GPIO

import ephem
import datetime as dt
from datetime import datetime, timezone
from math import *
toDeg = 180 / pi
toRad = pi / 180

tle_string = """
ONEWEB-0039             
1 45146U 20008R   21222.48564789 -.00000547  00000-0 -16045-2 0  9996
2 45146  87.8855  28.4737 0002346  81.2474 278.8919 13.10371370 76132
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

DIR_Az_Pin = 2
STEP_Az_Pin = 3
azDirection = 0

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

def singleStep_Az():
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

if riseAzimuth > setAzimuth :
    GPIO.output(DIR_Az_Pin, 0)
    azDirection = 0
else:
    GPIO.output(DIR_Az_Pin, 1)
    azDirection = 1

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


    if (currYAngle) < (satellite.alt * toDeg):
        print("ystep")
        singleStep_Elev(1)
        currYAngle = currYAngle + 0.9
    elif (currYAngle) >= (satellite.alt * toDeg):
        print("ystep")
        singleStep_Elev(0)
        currYAngle = currYAngle - 0.9

    if not azDirection:
        if (currXAngle % 360) < (satellite.az * toDeg) :
            print("xstep")
            singleStep_Az()
            currXAngle = currXAngle + 0.36
        if (currXAngle % 360) > (satellite.az * toDeg) :
            print("xstep")
            singleStep_Az()
            currXAngle = currXAngle - 0.36
GPIO.cleanup()