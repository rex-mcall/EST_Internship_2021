import serial
import time
import string
import pynmea2

port="/dev/ttyAMA0"
ser=serial.Serial(port, baudrate=9600, timeout=0.5)
while True:
    newdata=ser.readline()
    try:
        pass
        #print(newdata.decode())
    except:
        pass
    if newdata.decode()[0:6] == '$GPGGA':
        print("in if")
        newmsg = pynmea2.parse(newdata)
        lat = newmsg.latitude
        lng = newmsg.longitude
        gps = "Latitude = " + str(lat) + "and Longitude = " + str(lng)
        print(gps)