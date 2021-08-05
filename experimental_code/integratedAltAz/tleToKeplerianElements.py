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
toDeg = 180 / pi

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
    ecc = calc_eccentricity(tle)
    E = M
    nextE = E - ((E - (ecc * sin(E - M))) / (1 - ecc * cos(E)))
    while (abs((nextE - E) / nextE) > 1e-14):
        E = nextE
        # both versions of the equation yield the same answer
        # nextE = (((M) - (ecc * (E * math.cos(E) - math.sin(E)))) / (1 - ecc * math.cos(E)))
        nextE = E - ((E - (ecc * sin(E)) - M) / (1 - (ecc * cos(E))))
    return E


# calculates the true anomaly at the TLE epoch
def calc_truea(tle):
    M = calc_M(tle)
    E = calc_E(tle)
    ecc = calc_eccentricity(tle)
    truea = 2 * atan2(sqrt(1 + ecc) * sin(E / 2), sqrt(1 - ecc) * cos(E / 2))
    return truea


#calculates the true anomaly for a given delta in seconds after the TLE epoch time
def calc_truea_deltaT(tle, deltaTSeconds) :
    M = calc_M(tle)
    ecc = calc_eccentricity(tle)
    n = calc_n(tle)
    M = M + (n * deltaTSeconds)
    # same as calc_E except is propogates the mean anomaly forward in time
    E = M
    nextE = E - ((E - (ecc * sin(E - M))) / (1 - ecc * cos(E)))
    while (abs((nextE - E) / nextE) > 1e-14):
        E = nextE
        # both versions of the equation yield the same answer
        # nextE = (((M) - (ecc * (E * math.cos(E) - math.sin(E)))) / (1 - ecc * math.cos(E)))
        nextE = E - ((E - (ecc * sin(E)) - M) / (1 - (ecc * cos(E))))
    v = 2 * atan2(sqrt(1 + ecc) * sin(E / 2), sqrt(1 - ecc) * cos(E / 2))
    return v

# returns the calculated orbital elements from a TLE set
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