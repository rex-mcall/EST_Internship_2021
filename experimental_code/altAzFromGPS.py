from math import *
import numpy as np

eqRadius = 6378 #a
polarRadius = 6356 #b


# calculates the Earth Centered, Earth Fixed vector for a given latitude, longitude, and height
# https://en.wikipedia.org/wiki/Geographic_coordinate_conversion#From_geodetic_to_ECEF_coordinates
def calcECEF(lat, lon, h):

    e2 = 1 - ( (polarRadius ** 2) / (eqRadius ** 2) )
    N = eqRadius / ((1 - e2 * sin(lat)) ** (1/2))
    magnitude = eqRadius + h

    ECEF_X = (N + magnitude) * cos(lat) * cos(lon)
    ECEF_Y = (N + magnitude) * cod(lat) * sin(lon)
    ECEF_Z = ((((polarRadius ** 2) / (eqRadius ** 2)) * N) + magnitude) * sin(lat)

    return ECEF_X, ECEF_Y, ECEF_Z

# computes the LOS vector
def computeLineOfSightVector(satXYZ, recXYZ) :
    satX, satY, satZ = satXYZ
    recX, recY, recZ = recXYZ

    losX = satX - recX
    losY = satY - recY
    losZ = satZ - recZ

    return losX, losY, losZ

