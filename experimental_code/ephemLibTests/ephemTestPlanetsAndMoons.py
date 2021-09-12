import ephem
import datetime as dt
import gps

sso = ephem.Jupiter()

observer = ephem.Observer()
#convert to Angle type by multiplying ephem.degree
observer.lat = gps.latitude * ephem.degree
observer.lon = gps.longitude * ephem.degree
observer.elev = 13
observer.date = dt.datetime.utcnow()

sso.compute(observer)

x = observer.next_pass(sso, singlepass=False)
# satellite.alt is a special Angle type. Multuiplying by 180/pi converts to normal degrees
print("alt = ", sso.alt)
print("az  = ", sso.az )
print("----")
print("alt = ", sso.alt * (180 / 3.14))
print("az  = ", sso.az  * (180 / 3.14))