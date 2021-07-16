# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from tletools import TLE
import matplotlib.pyplot as plt
import numpy as np
import math
import sys

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Constants
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

gravParam = 3.986004418 * (10 ** 14)
pi = math.pi
toRad = pi / 180
toDec = 180 / pi

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Variables
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Kepler Vars
ecc   = 0 # eccentricity
sma   = 0 # semimajor axis rad
inc   = 0 # inclination rad
lan   = 0 # longitude of ascending node rad
argp  = 0 # argument of periapsis rad
truea = 0 # true anomaly rad

n     = 0 # mean motion rad/sec
M     = 0 # mean anomaly rad
E     = 0 # eccentric anomaly

#true anomaly plot
epochX = [] #time
trueaY = [] #true anomaly

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Parse TLE
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
tle_string = """
ANIK F3                 
1 31102U 07009A   21196.24136359  .00000003  00000-0  00000-0 0  9998
2 31102   0.0282 284.2796 0001947 194.6993 142.5050  1.00274779 28533
"""

tle_string2 = """    
THEMIS D                
1 30797U 07004D   21196.24406038 -.00000504  00000-0  00000-0 0  9993
2 30797  13.3878   1.4559 8372317 117.8341 295.0692  0.87839905 25265
"""

tle_lines = tle_string.strip().splitlines()

tle = TLE.from_lines(*tle_lines)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# TLE to Keplerian Elements
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def calc_lan (tle) :
    global lan 
    lan = (tle.raan * toRad)
    return lan

def calc_argp (tle) :
    global argp
    argp = (tle.argp * toRad)

    return argp

def calc_inc (tle) :
    global inc
    inc = (tle.inc * toRad)

    return inc

def calc_eccentricity (tle) :
    global ecc
    ecc = (tle.ecc)

    return ecc

def calc_n (tle) :
    global n
    n = float(tle.n) * ( (1.0/86400.0) * (2.0 * pi) )

    return n

def calc_sma (tle) :
    global sma
    sma = (gravParam / (n ** 2)) ** (1.0/3.0)

    return sma

def calc_M (tle) :
    global M
    M = tle.M * toRad
    return M

def calc_truea (tle) :
    global M
    global truea
    global E

    # M + (n * deltaT) to calculate for points forward in time (90 min for iss)

    nextE = M

    while ( abs((nextE - E) / nextE) > 0.00001) :
        E = nextE
        nextE = M + (ecc * math.sin(E))
    
    truea = math.acos( (math.cos(E) - ecc) / (1.0 - ecc * math.cos(E)) )

    return truea

def calc_truea_time(tle, increment, numSeconds) :
    global epochX
    global trueaY
    global E
    global M
    epochX = []
    trueaY = []
    def my_range(start, end, step):
        while start <= end:
            yield start
            start += step
    for i in my_range (0, numSeconds, 60):
        nextE = M + (n * i)

        while ( abs((nextE - E) / nextE) > 0.00001) :
            E = nextE
            nextE = (M + (n * i)) + (ecc * math.sin(E))
        
        epochX.append(i / 60.0)
        trueaY.append( 2 * (math.atan2( (((1+ecc)**(1/2)) * math.sin(E/2)), (((1-ecc)**(1/2)) * math.cos(E/2) )) ) )


def tle_to_kepler () :
    calc_lan(tle)
    calc_argp(tle)
    calc_inc(tle)
    calc_eccentricity(tle)
    calc_n(tle)
    calc_M(tle)
    calc_sma(tle)
    #calc_truea(tle)

def main() :
    tle_to_kepler()

    # print("Longitude of Ascending Node (rad):     ", lan)
    # print("Argument of Perigee         (rad):     ", argp)
    # print("Inclination                 (rad):     ", inc)
    print("Eccentricity:                          ", ecc)
    # print("Semimajor Axis              (meters):  ", sma)
    # print("Semimajor Axis              (km):      ", sma / 1000)
    # print("True Anomaly                (rad):     ", truea)

    calc_truea_time(tle, 60, 57600 * 3)
    plt.plot(epochX, trueaY, label = "true anomaly")
    plt.legend()
    plt.show()

main()
