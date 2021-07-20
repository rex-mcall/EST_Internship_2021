import tleToTrueAnomaly as ttte
import tleData
from math import *
import matplotlib.pyplot as plt


# uses TLE to return the current distance to the focus
def distanceToCentralBody(tle, curr_trueA):
    lan, argp, inc, ecc, n, M, a, E, v = ttte.tleToKepler(tle)
    eccA = atan2(sqrt(1 - ecc ** 2) * sin(curr_trueA), ecc + cos(curr_trueA))
    eccA = eccA % (2 * pi)
    r = a * (1 - ecc * cos(eccA))
    return r

# calculates the cartesian coordinates for one point in time
def getOrbitalCartesianCoords(tle, curr_trueA):
    r = distanceToCentralBody(tle, curr_trueA)
    x = r * cos(curr_trueA)
    y = r * sin(curr_trueA)
    return x, y

# takes a tuple of true anomaly and epoch arrays and returns arrays of the calculated 
# orbital frame Cartesian coordinates for each point
def cartesianCoordsTime(tle, trueAnomalyTuple):
    epoch, trueAnomalyArray = trueAnomalyTuple
    orbitalPositionsX = []
    orbitalPositionsY = []

    for trueA in trueAnomalyArray:
        cartCoordX, cartCoordY = getOrbitalCartesianCoords(tle, trueA)
        orbitalPositionsX.append(cartCoordX)
        orbitalPositionsY.append(cartCoordY)

    return orbitalPositionsX, orbitalPositionsY