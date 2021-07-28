from tletools import TLE
import matplotlib.pyplot as plt
import numpy as np
import math
from math import *
import sys
import datetime as dt

import tleToKeplerianElements as ttke

# uses TLE to return the current distance of the satellite to the focus
def distanceToCentralBody(tle, curr_trueA):
    lan, argp, inc, ecc, n, M, a, E, v = ttke.tleToKepler(tle)
    eccA = atan2(sqrt(1 - ecc ** 2) * sin(curr_trueA), ecc + cos(curr_trueA))
    eccA = eccA % (2 * pi)
    r = a * (1 - ecc * cos(eccA))
    return r

# calculates the orbital plane cartesian coordinates for one point in time
def getOrbitalCartesianCoords(tle, curr_trueA):
    r = distanceToCentralBody(tle, curr_trueA)
    x = r * cos(curr_trueA)
    y = r * sin(curr_trueA)
    return x, y