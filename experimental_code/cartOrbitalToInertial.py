import keplerToCartesianOrbital as ktco
import tleToTrueAnomaly as ttte
import tleData
from math import *
import matplotlib.pyplot as plt

# takes a set of points in the orbital frame and converts them to a 
# 3d vector in the inertial frame oriented with Aries and equatorial plane
def getInterialFramePoints(tle, xy):
    orbX, orbY = xy  # orbital frame coords
    lan, argp, inc, ecc, n, M, a, E, v = ttte.tleToKepler(tle)

    # inertial frame coords
    inertX = (
        (orbX * ((cos(argp) * cos(lan)) - (sin(argp) * cos(inc) * sin(lan)))) -
        (orbY * ((sin(argp) * cos(lan)) - (cos(argp) * cos(inc) * sin(lan))))
    )

    inertY = (
        (orbX * ((cos(argp) * sin(lan)) + (sin(argp) * cos(inc) * cos(lan)))) +
        (orbY * ((cos(argp) * cos(inc * cos(lan)) - (sin(argp) * sin(lan)))))
    )

    inertZ = (
        (orbX * (sin(argp) * sin(inc))) +
        (orbY * (cos(argp) * cos(inc)))
    )

    return inertX, inertY, inertZ

#tuple of orbital positions X and Y arrays to arrays of inertial XYZ
def inertialFramePointsTime(tle, orbXY) :
    orbX, orbY = orbXY
    inertialX = []
    inertialY = []
    inertialZ = []

    for i in range(0, len(orbX)):
        x, y, z = getInterialFramePoints(tle, (orbX[i], orbY[i]))
        inertialX.append(x)
        inertialY.append(y)
        inertialZ.append(z)

    return inertialX, inertialY, inertialZ

