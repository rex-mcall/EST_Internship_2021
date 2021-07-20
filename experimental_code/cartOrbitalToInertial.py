import keplerToCartesianOrbital as ktco
import tleToTrueAnomaly as ttte
import tleData
from math import *
import matplotlib.pyplot as plt


def getInterialFramePoints(tle, xy):
    orbX, orbY = xy  # orbital frame coords
    lan, argp, inc, ecc, n, M, a, E, v = ttte.tleToKepler(tle)

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
