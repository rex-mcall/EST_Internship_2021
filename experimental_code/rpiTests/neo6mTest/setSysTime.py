import datetime as dt
import os
import sys

time  = dt.datetime(2021, 8, 27, 12, 7, 20)
yr = ((str)(time.year))
mon = ((str)(time.month)).zfill(2)
day = ((str)(time.day)).zfill(2)

hr  = ((str)(time.hour)).zfill(2)
min = ((str)(time.minute)).zfill(2)
sec = ((str)(time.second)).zfill(2)
systemutc = yr + mon + day + ' ' + hr + ':' + min + ':' + sec
os.system('sudo date -u --set="%s"' % systemutc)

print(dt.datetime.now(timezone.utc))