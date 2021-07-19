from tletools import TLE

tle_string1 = """
ISS
1 25544U 98067A   21198.56478412  .00002105  00000-0  46633-4 0  9992
2 25544  51.6430 192.5034 0001891 164.4186 332.7734 15.48814968293304
"""

#parses the TLE into a usable format
tle_lines1 = tle_string1.strip().splitlines()
tle1 = TLE.from_lines(*tle_lines1)
x = tle1.epoch
print(tle1.epoch)




def epochToJulianTime (tle) :
    return tle.epoch.jd

def julianToGMST (julDate) :
    tUT1 = (
        (julDate - 2451545.0) / 36525
    )

    thetaGMST = ( #Grenwich mean siderial time???
        67310.5841 + ((876600 + 8640184.212566) * tUT1) + (0.093104 * (tUT1 ** 2)) - (6.2e-6 * (tUT1 ** 3))
    )

    angleSecToTimeSec = 360 - ((thetaGMST % 86400) / 240)

    return angleSecToTimeSec