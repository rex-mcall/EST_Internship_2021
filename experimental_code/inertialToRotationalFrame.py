from math import *


def epochToJulianTime(tle):
    return tle.epoch.jd


def julianToGMST(julDate):
    tUT1 = (
        (julDate - 2451545.0) / 36525
    )

    thetaGMST = (  # Grenwich mean siderial time
        67310.5841 + ((876600 + 8640184.212566) * tUT1) + (0.093104 * (tUT1 ** 2)) - (6.2e-6 * (tUT1 ** 3))
    )

    angleSecToTimeSec = 360 - ((thetaGMST % 86400) / 240)

    return angleSecToTimeSec
