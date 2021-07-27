# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 2021 Rex McAllister
# https://downloads.rene-schwarz.com/download/M001-Keplerian_Orbit_Elements_to_Cartesian_State_Vectors.pdf
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from tletools import TLE
import matplotlib.pyplot as plt
import numpy as np
import math
from math import *
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


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# TLE to Keplerian Elements
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# converts the longitude of the ascending node from TLE degrees to radians
def calc_lan(tle):
    lan = (tle.raan * toRad)
    return lan


# converts the argument of perigee from TLE degrees to radians
def calc_argp(tle):
    argp = (tle.argp * toRad)
    return argp


# converts the inclination from TLE degrees to radians
def calc_inc(tle):
    inc = (tle.inc * toRad)
    return inc


# returns the native format of eccentricity from TLE
def calc_eccentricity(tle):
    ecc = (tle.ecc)
    return ecc


# converts the mean motion from TLE rev/day to rad/s
def calc_n(tle):
    n = float(tle.n) * ((1.0/86400.0) * (2.0 * pi))
    return n


# calculates the length of the semimajor axis in kilometers
def calc_sma(tle):
    n = calc_n(tle)
    sma = (gravParam / (n ** 2)) ** (1.0/3.0)
    return sma


# converts the mean anomaly from TLE degrees to radians
def calc_M(tle):
    M = tle.M * toRad
    return M


# calculates the eccentric anomaly (rad) using a Newton-Rhapson setup
def calc_E(tle):
    M = calc_M(tle)
    nextE = M
    E = nextE
    while (abs((nextE - E) / nextE) > 0.00001):
        E = nextE
        nextE = (((M) - (ecc * (E * math.cos(E) - math.sin(E)))) /
                 (1 - ecc * math.cos(E)))
    return E


# calculates the true anomaly (rad)
def calc_truea(tle):
    M = calc_M(tle)
    E = calc_E(tle)
    ecc = calc_eccentricity(tle)

    truea = 2 * atan2(sqrt(1 + ecc) * sin(E / 2), sqrt(1 - ecc) * cos(E / 2))

    return truea


# creates an array of the value of true anomaly for a period of time over the orbit
def calc_truea_time(tle, increment, numSeconds):
    E = calc_E(tle)
    M = calc_M(tle)
    ecc = calc_eccentricity(tle)
    n = calc_n(tle)
    epochX = []
    trueaY = []

    def my_range(start, end, step):
        while start <= end:
            yield start
            start += step
    for i in my_range(0, numSeconds, 60):
        # same as calc_E except is propogates the mean anomaly forward in time
        nextE = M + (n * i)

        while (abs((nextE - E) / nextE) > 0.00001):
            E = nextE
            #nextE = (M + (n * i)) + (ecc * math.sin(E))
            nextE = (((M+(n*i)) - (ecc * (E * math.cos(E) - math.sin(E)))
                      ) / (1 - ecc * math.cos(E)))

        epochX.append(i / 60.0)

        # trueaY.append(2 * math.atan( (((1.0+ecc) / (1.0-ecc))**(1.0/2.0)) * math.tan(E/2.0)))

        trueaY.append(2 * atan2(sqrt(1 + ecc) * sin(E / 2),
                      sqrt(1 - ecc) * cos(E / 2)))
    return epochX, trueaY


# returns a dictionary of calculated orbital elements for a TLE
def tleToKepler(tle):

    lan = calc_lan(tle)           # longitude ascending node
    argp = calc_argp(tle)         # argument periapsis
    inc = calc_inc(tle)           # inclination
    ecc = calc_eccentricity(tle)  # eccentricity
    n = calc_n(tle)               # mean motion
    M = calc_M(tle)               # mean anomaly
    a = calc_sma(tle)             # semimajor axis
    E = calc_E(tle)               # eccentric anomaly
    v = calc_truea(tle)           # true anomaly

    return lan, argp, inc, ecc, n, M, a, E, v