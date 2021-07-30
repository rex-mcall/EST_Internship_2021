from tletools import TLE

tle_string1 = """
ISS
1 25544U 98067A   21208.30146631 -.00003369  00000-0 -53333-4 0  9991
2 25544  51.6439 144.3575 0001405 200.4665 262.5751 15.48855261294819
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

tle_string3 = """
STARLINK-1558           
1 46035U 20055J   21208.20896115  .00001241  00000-0  10222-3 0  9993
2 46035  53.0555 137.5338 0001496  70.0053 290.1097 15.06391114 54185
"""

tle_lines3 = tle_string3.strip().splitlines()
tle3 = TLE.from_lines(*tle_lines3)