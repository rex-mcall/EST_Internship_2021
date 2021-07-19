import experimental_code.keplerToCartesianOrbital as ktco
from math import *
import matplotlib.pyplot as plt


def getInterialFramePoints (tle, xy) :
    orbitalX, orbitalY = xy #orbital frame coords
