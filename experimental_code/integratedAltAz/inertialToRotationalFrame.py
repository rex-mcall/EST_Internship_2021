from tletools import TLE
import matplotlib.pyplot as plt
import numpy as np
import math
from math import *
import sys
import datetime as dt

gravParam = 3.986004418 * (10 ** 14)
pi = math.pi
toRad = pi / 180
toDec = 180 / pi

# helper function to grab the julian date from the TLE
def epochToJulianTime(tle):
    return tle.epoch.jd

# returns the julian time of a datetime object
def datetimeToJulianTime(x):
    jd = (
        (367 * x.year) - 
        int((7 * (x.year + int((x.month + 9) / 12))) / 4) + 
        int((275 * x.month) / 9) + 
        x.day + 
        1721013.5 + 
        ((((((x.second + (x.microsecond / 1e6)) / 60) + x.minute) / 60) + x.hour) / 24)
    )
    return jd
# calculates the angle to rotate between GMT and the reference direction towards Aries
# angle between GMT line and aries heading
def julianToGMST(julDate):
    tUT1 = (
        (julDate - 2451545.0) / 36525
    )

    thetaGMST = (  # Grenwich mean siderial time
        67310.54841 + ((876600 + 8640184.812866) * tUT1) + (0.093104 * (tUT1 ** 2)) - (6.2e-6 * (tUT1 ** 3))
    )

    angleSecToTimeSec = 360 - ((thetaGMST % 86400) / 240)

    return angleSecToTimeSec * toRad

# uses the CCW Z-axis rotation matrix to rotate to the new GMST angle
# moves from inertial frame to rotational frame (ECEF coords)
# julianDate is the observation time and inertXYZ are inertial coords
# https://www.mathworks.com/help/phased/ref/rotz.html
def matrixRotation (tle, inertXYZ, julianDate) :
    inertX, inertY, inertZ = inertXYZ

    inertMatrix = np.array([
        inertX,
        inertY,
        inertZ
    ])

    rotationAngle = julianToGMST(julianDate)
    # rotationAngle = 237.77 * toRad

    rotationMatrix = np.array([
        [cos(rotationAngle), -sin(rotationAngle), 0],
        [sin(rotationAngle),  cos(rotationAngle), 0],
        [0,                   0,                  1]
    ])

    numpyRotatedCoords = np.dot(rotationMatrix, inertMatrix)
    rotatedCoords = numpyRotatedCoords.tolist()
    
    return rotatedCoords[0], rotatedCoords[1], rotatedCoords[2]