# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from tletools import TLE
import math
import sys

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Constants
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

gravParam = 3.986004418 * (10 ** 14)
pi = math.pi
toRad = pi / 180

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Variables
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Kepler Vars
ecc   = 0 # eccentricity
sma   = 0 # semimajor axis rad
inc   = 0 # inclination rad
lan   = 0 # longitude of ascending node rad
argp  = 0 # argument of periapsis rad
truea = 0 # true anomaly rad

n     = 0 # mean motion rad/sec
M     = 0 # mean anomaly rad
E     = 0 # eccentric anomaly

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Parse TLE
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
tle_string = """
ISS (ZARYA)
1 25544U 98067A   21195.53225064  .00001295  00000-0  31859-4 0  9992
2 25544  51.6422 207.5031 0001965 161.3238 336.1898 15.48797358292834
"""

tle_lines = tle_string.strip().splitlines()

tle = TLE.from_lines(*tle_lines)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# TLE to Keplerian Elements
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def calc_lan (tle) :
    global lan 
    lan = (tle.raan * toRad)

def calc_argp (tle) :
    global argp
    argp = (tle.argp * toRad)

def calc_inc (tle) :
    global inc
    inc = (tle.inc * toRad)

def calc_eccentricity (tle) :
    global ecc
    ecc = (tle.ecc)

def calc_sma (tle) :
    global sma
    global n
    global T
    n = float(tle.n) * ( (1.0/86400.0) * (2.0 * pi) )
    sma = (gravParam ** (1.0/3.0)) / ((2 * tle.n * pi) ** (2.0/3.0))

def calc_truea (tle) :
    global M
    global truea
    global E
    M = tle.M * toRad

    nextE = M

    while ( abs((nextE - E) / nextE) > 0.01) :
        E = nextE
        nextE = M + (ecc * math.sin(E))
    
    truea = math.acos( (math.cos(E) - ecc) / (1.0 - ecc * math.cos(E)) )

def tle_to_kepler () :
    calc_lan(tle)
    calc_argp(tle)
    calc_inc(tle)
    calc_eccentricity(tle)
    calc_sma(tle)
    calc_truea(tle)

tle_to_kepler()

print("Longitude of Ascending Node: ", lan)
print("Argument of Perigee: ", argp)
print("Inclination: ", inc)
print("Eccentricity: ", ecc)
print("Semimajor Axis", sma)
print("True Anomaly", truea)
