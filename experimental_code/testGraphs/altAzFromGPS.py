from math import *
import numpy as np

eqRadius = 6378000 #a
polarRadius = 6356000 #b


# calculates the Earth Centered, Earth Fixed [ECEF] vector for a ground station latitude, longitude, and height
# latitude & longitude in decimal, height in GPS height above mean sea level in meters
# https://en.wikipedia.org/wiki/Geographic_coordinate_conversion#From_geodetic_to_ECEF_coordinates
def calcECEF(lat, lon, h):

    e2 = 1 - ( (polarRadius ** 2) / (eqRadius ** 2) )
    N = eqRadius / ((1 - e2 * sin(lat)) ** (1/2))
    magnitude = eqRadius + h

    ECEF_X = (N + magnitude) * cos(lat) * cos(lon)
    ECEF_Y = (N + magnitude) * cos(lat) * sin(lon)
    ECEF_Z = ((((polarRadius ** 2) / (eqRadius ** 2)) * N) + magnitude) * sin(lat)

    return ECEF_X, ECEF_Y, ECEF_Z

# computes the LOS vector in ECEF coordinates between the satellite and reveiver
def computeLineOfSightVector(satXYZ, recXYZ) :
    satX, satY, satZ = satXYZ
    recX, recY, recZ = recXYZ

    losX = satX - recX
    losY = satY - recY
    losZ = satZ - recZ

    return losX, losY, losZ


def calcAltAz(satXYZ, recXYZ, lat, lon, h):
    losX, losY, losZ = computeLineOfSightVector(satXYZ, recXYZ)

    losMatrix = [
        losX,
        losY,
        losZ
    ]

    sezRotationMatrix = np.array([
        [sin(lat)*cos(lon),   sin(lat)*sin(lon),   -cos(lat)  ],
        [-sin(lon)        ,    cos(lon)        ,   0          ],
        [cos(lat)*cos(lon),   cos(lat)*sin(lon),   sin(lat)   ]
    ])

    numpySEZ = np.dot(sezRotationMatrix, losMatrix)
    sezArray = numpySEZ.tolist()

    #vector norm of SEZ
    sezMagnitude = (
        ( (sezArray[0] ** 2) + 
          (sezArray[1] ** 2) + 
          (sezArray[2] ** 2) ) ** (1/2)
    )

    altitude = asin(sezArray[2] / sezMagnitude)
    azimuth = atan2(sezArray[1], -sezArray[0])

    return altitude, azimuth





