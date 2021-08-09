import ephem
import datetime
import gps
import tleData as tled

observer = ephem.Observer()
observer.lat = gps.latitude
observer.lon = gps.longitude

