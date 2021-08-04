from astropy import coordinates as coord

from astropy import units as u

from astropy.time import Time

now = Time('2021-07-27 05:00:54')

# position of satellite in GCRS or J20000 ECI:

cartrep = coord.CartesianRepresentation(x=-5113262.263019504,

                                        y=4670155.874058677,

                                        z=9553.552285500802,
                                        
                                        unit=u.m)

gcrs = coord.GCRS(cartrep, obstime=now)

itrs = gcrs.transform_to(coord.ITRS(obstime=now))

print(itrs)