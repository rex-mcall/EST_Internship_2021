import tleToTrueAnomaly          as ttte
import keplerToCartesianOrbital  as ktco
import cartOrbitalToInertial     as coti
import inertialToRotationalFrame as itrf
import tleData                   as tled

from math import *
import matplotlib.pyplot as plt


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# tleToTrueAnomaly
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Test code to plot points over time to make sure the functions work correctly
def plot_tle_over_time():
    epochX, trueaY = ttte.calc_truea_time(tled.tle2, 120, 5760 * 6)
    plt.plot(epochX, trueaY, label="true anomaly")
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




def main() :
    # tleToTrueAnomaly
    plot_tle_over_time()

    # keplerToCartesianOrbital
    truea1 = ttte.calc_truea_time(tled.tle1, 120, 5760 * 6)
    truea2 = ttte.calc_truea_time(tled.tle2, 120, 5760 * 6)
    plotCartesianCoords(tled.tle1, ktco.cartesianCoordsTime(tled.tle1, truea1), tled.tle2, ktco.cartesianCoordsTime(tled.tle2, truea2))



main()