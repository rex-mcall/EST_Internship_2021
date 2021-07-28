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
STARLINK-2614           
1 48380U 21038AD  21207.42244936  .00001160  00000-0  96783-4 0  9998
2 48380  53.0545   6.0437 0001401 101.4790 258.6356 15.06388799 12852
"""

tle_lines3 = tle_string3.strip().splitlines()
tle3 = TLE.from_lines(*tle_lines3)