from tletools import TLE
import matplotlib.pyplot as plt
import numpy as np
import math
from math import *
import sys
import datetime as dt

import tleToKeplerianElements      as ttke
import keplerianToCartesianOrbital as ktco
import cartesianOrbitalToInertial  as coti
import inertialToRotationalFrame   as itrf
import tleData                     as tled
import gps

gravParam = 3.986004418 * (10 ** 14)
pi = math.pi
toRad = pi / 180
toDec = 180 / pi

eqRadius = 6378 #a, radius of earth at equator
polarRadius = 6356 #b, radius of earth at poles

# calculates the Earth Centered, Earth Fixed [ECEF] vector for a ground station latitude, longitude, and height
# latitude & longitude in decimal, height in GPS height above mean sea level in meters
# https://en.wikipedia.org/wiki/Geographic_coordinate_conversion#From_geodetic_to_ECEF_coordinates
def calcECEF(lat, lon, h):

    e2 = 1 - ( (polarRadius ** 2) / (eqRadius ** 2) )
    N = eqRadius / ((1 - e2 * sin(lat)) ** (1/2))
    magnitude = eqRadius + h

    ECEF_X = (N + magnitude) * cos(lat) * cos(lon)
    ECEF_Y = (N + magnitude) * cos(lat) * sin(lon)
    ECEF_Z = ((((polarRadius ** 2) / (eqRadius ** 2)) * N) + magnitude) * sin(lat)

    return ECEF_X, ECEF_Y, ECEF_Z

# computes the LOS vector in ECEF coordinates between the satellite and reveiver
def computeLineOfSightVector(satXYZ, recXYZ) :
    satX, satY, satZ = satXYZ
    recX, recY, recZ = recXYZ

    losX = satX - recX
    losY = satY - recY
    losZ = satZ - recZ

    return losX, losY, losZ


def calcAltAz(satXYZ, recXYZ, lat, lon, h):
    losX, losY, losZ = computeLineOfSightVector(satXYZ, recXYZ)

    losMatrix = [
        losX,
        losY,
        losZ
    ]

    sezRotationMatrix = np.array([
        [sin(lat)*cos(lon),   sin(lat)*sin(lon),   -cos(lat)  ],
        [-sin(lon)        ,    cos(lon)        ,   0          ],
        [cos(lat)*cos(lon),   cos(lat)*sin(lon),   sin(lat)   ]
    ])

    # sezRotationMatrix = np.array([
    #     [-sin(lat)        ,    cos(lat)        ,   0          ],
    #     [sin(lon)*cos(lat),   sin(lon)*sin(lat),   -cos(lon)  ],
    #     [cos(lon)*cos(lat),   cos(lon)*sin(lat),   sin(lon)   ]
    # ])

    numpySEZ = np.dot(sezRotationMatrix, losMatrix)
    sezArray = numpySEZ.tolist()

    #vector norm of SEZ
    sezMagnitude = (
        ( (sezArray[0] ** 2) + 
          (sezArray[1] ** 2) + 
          (sezArray[2] ** 2) ) ** (1/2)
    )

    azimuth = atan2(sezArray[1], -sezArray[0])
    altitude = asin(sezArray[2] / sezMagnitude)

    return altitude, azimuth

# calculates the altitude and azimuth given a TLE
# object, reveiver location in decimal coords, and
# a datetime object of viewing time
def main(tle, recLat, recLon, recH, currTime):

    timeDifference = currTime - tle.epoch.datetime
    elapsedSeconds = timeDifference.total_seconds()

    currTrueAnom = ttke.calc_truea_deltaT(tle, elapsedSeconds)
    orbX, orbY = ktco.getOrbitalCartesianCoords(tle, currTrueAnom)

    inertX, inertY, inertZ = coti.getInterialFramePoints(tle, (orbX, orbY))

    julianTime = itrf.datetimeToJulianTime(currTime)
    rotX, rotY, rotZ = itrf.matrixRotation(tle, (inertX, inertY, inertZ), julianTime)

    recPosTuple = calcECEF(gps.latitude, gps.longitude, gps.height)

    altAz = calcAltAz((rotX, rotY, rotZ), recPosTuple, gps.latitude, gps.longitude, gps.height)

    print("Altitude  : ", altAz[0])
    print("Azimuth   : ", altAz[1])

x = dt.datetime(2021, 7, 28, 3, 4, 19)

main(tled.tle3, gps.latitude, gps.longitude, gps.height, x)
