from math import *
import numpy as np

#helper function to grab the julian date from the TLE
def epochToJulianTime(tle):
    return tle.epoch.jd

#calculates the angle to rotate between GMT and the reference direction towards Aries
def julianToGMST(julDate):
    tUT1 = (
        (julDate - 2451545.0) / 36525
    )

    thetaGMST = (  # Grenwich mean siderial time
        67310.5841 + ((876600 + 8640184.212566) * tUT1) + (0.093104 * (tUT1 ** 2)) - (6.2e-6 * (tUT1 ** 3))
    )

    angleSecToTimeSec = 360 - ((thetaGMST % 86400) / 240)

    return angleSecToTimeSec

#uses the CCW Z-axis rotation matrix to rotate to the new GMST angle
# https://www.mathworks.com/help/phased/ref/rotz.html
def matrixRotation (tle, inertXYZ) :
    inertX, inertY, inertZ = inertXYZ

    inertMatrix = np.array([
        inertX,
        inertY,
        inertZ
    ])

    julDate = epochToJulianTime(tle)

    rotationAngle = julianToGMST(julDate)

    rotationMatrix = np.array([
        [cos(rotationAngle), -sin(rotationAngle), 0],
        [sin(rotationAngle),  cos(rotationAngle), 0],
        [0,                   0,                  1]
    ])

    numpyRotatedCoords = np.dot(rotationMatrix, inertMatrix)
    rotatedCoords = numpyRotatedCoords.tolist()


    # for i in range(len(inertMatrix)):
    #     for j in range (len(rotationMatrix[0])):
    #         for k in range (len(rotationMatrix)):
    #             rotatedCoords[i] += inertMatrix[i] * rotationMatrix[k][j]
    
    return rotatedCoords[0], rotatedCoords[1], rotatedCoords[2]

#takes a tuple of inertial XYZ arrays and moves them to the rotational frame (ECEF coords)
def matrixRotationTime(tle, inertXYZ) :
    inertX, inertY, inertZ = inertXYZ

    rotatedX = []
    rotatedY = []
    rotatedZ = []

    for i in range (0, len(inertX)) :
        x, y, z = matrixRotation(tle, (inertX[i], inertY[i], inertZ[i]))
        rotatedX.append(x)
        rotatedY.append(y)
        rotatedZ.append(z)

    return rotatedX, rotatedY, rotatedZ