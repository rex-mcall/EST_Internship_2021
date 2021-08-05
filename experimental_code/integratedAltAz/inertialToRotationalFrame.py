from tletools import TLE
import matplotlib.pyplot as plt
import numpy as np
import math
from math import *
import sys
import datetime as dt

import tleData as tled

gravParam = 3.986004418 * (10 ** 14)
pi = math.pi
toRad = pi / 180
toDeg = 180 / pi

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

def julianToGMST(julDate):
    D = julDate - 2451545.0
    GMST =  18.697374558 + (24.06570982441908 * D)
    hours = GMST % 24
    Angle = hours * 3600 * (7.2921159e-5)
    return Angle

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
        [cos(rotationAngle), sin(rotationAngle), 0],
        [-sin(rotationAngle),  cos(rotationAngle), 0],
        [0,                   0,                  1]
    ])

    numpyRotatedCoords = np.dot(rotationMatrix, inertMatrix)
    rotatedCoords = numpyRotatedCoords.tolist()
    
    return rotatedCoords[0], rotatedCoords[1], rotatedCoords[2]