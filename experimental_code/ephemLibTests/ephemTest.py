import ephem
import datetime
import gps

observer = ephem.Observer()
observer.lat = gps.latitude
observer.lon = gps.longitude

