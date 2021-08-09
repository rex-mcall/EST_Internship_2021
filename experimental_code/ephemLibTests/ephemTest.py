import ephem
import datetime as dt
import gps


tle_string3 = """
STARLINK-1558           
1 46035C 20055J   21221.47051397  .00004288  00000-0  28724-3 0  2210
2 46035  53.0547  78.0035 0001839  85.6035 232.0384 15.06402484    12
"""

tle_lines = tle_string3.strip().splitlines()
satellite = ephem.readtle(tle_lines[0], tle_lines[1], tle_lines[2])

observer = ephem.Observer()
#convert to Angle type by multiplying ephem.degree
observer.lat = gps.latitude * ephem.degree
observer.lon = gps.longitude * ephem.degree
observer.elev = 13
observer.date = dt.datetime(2021, 7, 28, 19, 24, 24)

satellite.compute(observer)


# satellite.alt is a special Angle type. Multuiplying by 180/pi converts to normal degrees
print("alt = ", satellite.alt)
print("az  = ", satellite.az )
print("----")
print("alt = ", satellite.alt * (180 / 3.14))
print("az  = ", satellite.az  * (180 / 3.14))

