import serial
import time
import string
import pynmea2

port="/dev/ttyAMA0"
ser=serial.Serial(port, baudrate=9600, timeout=0.5)
while True:
    try:
        newdata=ser.readline()
        data = newdata.decode()

        if data[0:6] == '$GPGGA':
            print("in if")
            newmsg = pynmea2.parse(data)
            lat = newmsg.latitude
            lng = newmsg.longitude
            gps = "Latitude = " + str(lat) + "and Longitude = " + str(lng)
            print(gps)
    except KeyboardInterrupt:
        exit()
    except Exception:
        pass