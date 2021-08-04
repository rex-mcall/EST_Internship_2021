from tletools import TLE
import matplotlib.pyplot as plt
import numpy as np
import math
from math import *
import sys
import datetime as dt

import tleToKeplerianElements as ttke

# takes a set of points in the orbital frame and converts them to a 
# 3d vector in the inertial frame oriented with Aries and equatorial plane
def getInterialFramePoints(tle, orbXY):
    orbX, orbY = orbXY  # orbital frame coords
    lan, argp, inc, ecc, n, M, a, E, v = ttke.tleToKepler(tle)

    # inertial frame coords
    inertX = (
        (orbX * ((cos(argp) * cos(lan)) - (sin(argp) * cos(inc) * sin(lan)))) -
        (orbY * ((sin(argp) * cos(lan)) + (cos(argp) * cos(inc) * sin(lan))))
    )

    inertY = (
        (orbX * ((cos(argp) * sin(lan)) + (sin(argp) * cos(inc) * cos(lan)))) +
        (orbY * ((cos(argp) * cos(inc) * cos(lan)) - (sin(argp) * sin(lan))))
    )

    inertZ = (
        (orbX * (sin(argp) * sin(inc))) +
        (orbY * (cos(argp) * sin(inc)))
    )
    return inertX, inertY, inertZ