import serial
import time
import string
import pynmea2
import datetime as dt
from datetime import datetime, timezone
import os
import sys

port="/dev/ttyAMA0"
ser=serial.Serial(port, baudrate=9600, timeout=0.5)

def runGPS_Interface():
    gotResult = False
    while not gotResult:
        try:
            currData=ser.readline()
            data = currData.decode()

            if data[0:6] == '$GPRMC':
                gotResult = True
                parsedNMEA = pynmea2.parse(data)
                setSysTime(parsedNMEA.datetime)
                lat = parsedNMEA.latitude
                long = parsedNMEA.longitude
                return lat, long
        except Exception:
            pass

def setSysTime(dtObject):
    yr = ((str)(dtObject.year))
    mon = ((str)(dtObject.month)).zfill(2)
    day = ((str)(dtObject.day)).zfill(2)

    hr  = ((str)(dtObject.hour)).zfill(2)
    min = ((str)(dtObject.minute)).zfill(2)
    sec = ((str)(dtObject.second)).zfill(2)
    systemutc = yr + mon + day + ' ' + hr + ':' + min + ':' + sec
    os.system('sudo date -u --set="%s"' % systemutc)