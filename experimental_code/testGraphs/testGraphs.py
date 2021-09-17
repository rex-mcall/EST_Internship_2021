import tleToTrueAnomaly          as ttte
import keplerToCartesianOrbital  as ktco
import cartOrbitalToInertial     as coti
import inertialToRotationalFrame as itrf
import altAzFromGPS              as aafg

import gps
import tleData                   as tled

from math import *
import matplotlib.pyplot as plt
import numpy as np


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# tleToTrueAnomaly
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Test code to plot points over time to make sure the functions work correctly
def plot_tle_over_time(tle):
    epochX, trueaY = ttte.calc_truea_time(tle, 120, 5760 * 6)
    plt.plot(epochX, trueaY, label="true anomaly")
    plt.xlabel("Minutes since TLE epoch")
    plt.ylabel("True Anomaly (radians)")
    plt.legend()
    plt.show()




# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# keplerToCartesianOrbital
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Test code to plot points over time to make sure the functions work correctly
def plotCartesianCoords(tle1, orbitalPositionsTuple1, tle2, orbitalPositionsTuple2):
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
    ax1.title.set_text(tle1.name)
    ax1.scatter(orbitalPositionsX1, orbitalPositionsY1)
    ax1.grid(b=True, which='both', axis='both')
    ax2.title.set_text(tle2.name)
    ax2.scatter(orbitalPositionsX2, orbitalPositionsY2)
    ax2.grid(b=True, which='both', axis='both')
    plt.show()

# plots the distance to the orbital body over time to confirm it is sinusoidal
def plot_data(dtcb):
    fig, ax = plt.subplots(1, 1)
    ax.scatter(range(0, dtcb.__len__()), dtcb)
    plt.show()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# cartOrbitalToInertial
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def plotOrbitalToInertial(tle) :
    epoch_tAnomArray = ttte.calc_truea_time(tle, 120, 5760 * 3)
    orbX, orbY = ktco.cartesianCoordsTime(tle, epoch_tAnomArray)

    inertX, inertY, inertZ = coti.inertialFramePointsTime(tle, (orbX, orbY))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection = "3d")
    ax.set_box_aspect((np.ptp(inertX), np.ptp(inertX), np.ptp(inertX)))  # aspect ratio is 1:1:1 in data space
    ax.scatter(inertX, inertY, inertZ, marker='o')

    plt.show()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# inertialToRotationalFrame
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def plotInertToRotation(tle) :
    epoch_tAnomArray = ttte.calc_truea_time(tle, 480, 5760 * 3)
    orbX, orbY = ktco.cartesianCoordsTime(tle, epoch_tAnomArray)

    inertX, inertY, inertZ = coti.inertialFramePointsTime(tle, (orbX, orbY))
    rotX, rotY, rotZ = itrf.matrixRotationTime(tle, (inertX, inertY, inertZ))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection = "3d")
    
    ax.scatter(inertX, inertY, inertZ, c='b', marker='o')
    ax.scatter(rotX, rotY, rotZ, c = 'r',marker='o')

    plt.show()

def testAltAz(tle) :
    epoch_tAnomArray = ttte.calc_truea_time(tle, 480, 5760 * 3)
    orbX, orbY = ktco.cartesianCoordsTime(tle, epoch_tAnomArray)

    inertX, inertY, inertZ = coti.inertialFramePointsTime(tle, (orbX, orbY))
    rotX, rotY, rotZ = itrf.matrixRotationTime(tle, (inertX, inertY, inertZ))

    recPosTuple = aafg.calcECEF(gps.latitude, gps.longitude, gps.height)

    altAz = aafg.calcAltAz((rotX, rotY, rotZ), recPosTuple, gps.latitude, gps.longitude, gps.height)

    print("Altitude  : ", altAz[0])
    print("Azimuth   : ", altAz[1])

def main() :
    # # tleToTrueAnomaly
    # plot_tle_over_time(tled.tle2)

    # # keplerToCartesianOrbital
    # truea1 = ttte.calc_truea_time(tled.tle1, 120, 5760 * 6)
    # truea2 = ttte.calc_truea_time(tled.tle2, 120, 5760 * 6)
    # plotCartesianCoords(tled.tle1, ktco.cartesianCoordsTime(tled.tle1, truea1), tled.tle2, ktco.cartesianCoordsTime(tled.tle2, truea2))

    # # # cartOrbitalToInertial
    plotOrbitalToInertial(tled.tle2)

    # inertialToRotationalFrame
    # plotInertToRotation(tled.tle2)

    # testAltAz(tled.tle2)
main()