from tletools import TLE

tle_string1 = """
ISS
1 25544U 98067A   21198.56478412  .00002105  00000-0  46633-4 0  9992
2 25544  51.6430 192.5034 0001891 164.4186 332.7734 15.48814968293304
"""

#parses the TLE into a usable format
tle_lines1 = tle_string1.strip().splitlines()
tle1 = TLE.from_lines(*tle_lines1)

tle_string2 = """    
TDO-4                   
1 48620U 21042C   21196.05607278  .00195249 -15658-5  58694-3 0  9999
2 48620  26.1589 138.3041 2377990 101.4959 285.9800 10.88066450  6184
"""

tle_lines2 = tle_string2.strip().splitlines()
tle2 = TLE.from_lines(*tle_lines2)
