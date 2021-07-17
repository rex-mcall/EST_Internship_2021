import tleToTrueAnomaly as ttte
from math import *
import matplotlib.pyplot as plt
import orbital.utilities

orbitalPositionsX = []
orbitalPositionsY = []
dtcb = []


#uses TLE to return the current distance to the focus
def distanceToCentralBody (tle, curr_trueA) :
    global dtcb
    keplerianElements = ttte.get_tle_to_kepler(tle)
    sma = keplerianElements["sMajorAxis"]
    ecc = keplerianElements["eccentricity"]
    eccA = atan2(sqrt(1 - ecc ** 2) * sin(curr_trueA), ecc + cos(curr_trueA))
    eccA = eccA % (2 * pi)
    r = sma * ( 1 - ecc * cos(eccA))
    dtcb.append(r)
    return r


def getOrbitalCartesianCoords (tle, curr_trueA) :
    keplerianElements = ttte.get_tle_to_kepler(tle)
    r = distanceToCentralBody(tle, curr_trueA)
    x = r * cos(curr_trueA)
    y = r * sin(curr_trueA)
    cartesianPoints = [x, y]
    return cartesianPoints

def cartesianCoordsTime (tle, trueAnomalyTuple) :
    epoch, trueAnomalyArray = trueAnomalyTuple
    orbitalPositionsX = []
    orbitalPositionsY = []

    for trueA in trueAnomalyArray:
        cartCoord = getOrbitalCartesianCoords(tle, trueA)
        orbitalPositionsX.append(cartCoord[0])
        orbitalPositionsY.append(cartCoord[1])
    
    return orbitalPositionsX, orbitalPositionsY

def plotCartesianCoords (orbitalPositionsTuple1, orbitalPositionsTuple2) :
    orbitalPositionsX1, orbitalPositionsY1 = orbitalPositionsTuple1
    orbitalPositionsX2, orbitalPositionsY2 = orbitalPositionsTuple2

    
    axisRange = 1.5e7

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_figheight(5)
    fig.set_figwidth(11)
    ax1.set_aspect(1)
    ax2.set_aspect(1)
    ax1.set_xlim(-axisRange, axisRange)
    ax1.set_ylim(-axisRange, axisRange)
    ax2.set_xlim(-axisRange, axisRange)
    ax2.set_ylim(-axisRange, axisRange)
    ax1.title.set_text(ttte.tle1.name)
    ax1.scatter(orbitalPositionsX1, orbitalPositionsY1)
    ax1.grid(b=True, which = 'both', axis='both')
    ax2.title.set_text(ttte.tle2.name)
    ax2.scatter(orbitalPositionsX2, orbitalPositionsY2)
    ax2.grid(b=True, which = 'both', axis='both')
    plt.show()

def plot_data(dtcb) :
    fig, ax = plt.subplots(1,1)
    ax.scatter(    range(0, dtcb.__len__()), dtcb)
    plt.show()

truea1 = ttte.calc_truea_time(ttte.tle1, 120, 5760 * 6)
truea2 = ttte.calc_truea_time(ttte.tle2, 120, 5760 * 6)
plotCartesianCoords(cartesianCoordsTime(ttte.tle1, truea1), cartesianCoordsTime(ttte.tle2, truea2))
#plot_data(dtcb)
