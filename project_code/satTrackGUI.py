from tkinter import *
import ephem
import datetime as dt
from datetime import datetime, timezone
from math import *
from functools import partial
from threading import Thread

from satSearch import *
from satDriver import *
import gpsInterface


class mainWindow():
    def __init__(self):

        # Master variable set --------------------------------------------------

        # calculated constants to convert to and from radians
        self.toDeg = 180 / pi
        self.toRad = pi / 180

        # sets up reveiver locaiton
        self.observer = ephem.Observer()
        #convert to Angle type by multiplying ephem.degree


        self.motors = motorInterface()


        # Initializing main window ---------------------------------------------
        self.master_window = Tk()
        self.master_window.title("Satellite Tracker")
        self.master_window.attributes("-fullscreen", True)
        # self.master_window.state("zoomed")

        # Top Buttons Frame ----------------------------------------------------
        self.buttons_frame = Frame(self.master_window)
        self.buttons_frame.pack(fill='y')

        self.btn_alternateMotorState = Button(self.buttons_frame, text='Enable Motors', command=self.alternateMotorState)
        self.btn_alternateMotorState.grid(row=0, column=0, padx=(10), pady=10)

        self.btn_Calibrate = Button(self.buttons_frame, text='Set Time & Location', command=self.setLocalization)
        self.btn_Calibrate.grid(row=0, column=1, padx=(10), pady=10)

        self.btn_Home = Button(self.buttons_frame, text='Home Motors', command=self.homeMotorsCommand)
        self.btn_Home.grid(row=0, column=2, padx=(10), pady=10)

        self.btn_closeApp = Button(self.buttons_frame, text='Exit Application', command=self.Close)
        self.btn_closeApp.grid(row=0, column=3, padx = 10, pady = 10)

        # Search Frame ----------------------------------------------------
        self.search_frame = Frame(self.master_window)
        self.search_frame.pack(fill='y')


        self.search_Text = Label(self.search_frame, text="Satellite Name:")
        self.search_Text.grid(row=0, column=0, padx=(10), pady=10)
        self.search_Entry = Entry(self.search_frame)
        self.search_Entry.grid(row=0, column=1, padx=(10), pady=10)


        self.minElev_Text = Label(self.search_frame, text="Minimum Vertex Elevation (Deg):")
        self.minElev_Text.grid(row=1, column=0, padx=(10), pady=10)
        self.minElev_Entry = Entry(self.search_frame)
        self.minElev_Entry.grid(row=1, column=1, padx=(10), pady=10)


        self.maxWait_Text = Label(self.search_frame, text="Max Wait Till Rise (Mins):")
        self.maxWait_Text.grid(row=2, column=0, padx=(10), pady=10)
        self.maxWait_Entry = Entry(self.search_frame)
        self.maxWait_Entry.grid(row=2, column=1, padx=(10), pady=10)

        self.minTimeLeft_Text = Label(self.search_frame, text="Min Time Left in Pass (Mins)")
        self.minTimeLeft_Text.grid(row=3, column=0, padx=(10), pady=10)
        self.minTimeLeft_Entry = Entry(self.search_frame)
        self.minTimeLeft_Entry.grid(row=3, column=1, padx=(10), pady=10)

        self.beforeVertex_Var = IntVar()
        self.beforeVertex_Text = Label(self.search_frame, text="Only Show Results Before Peak Elevation:")
        self.beforeVertex_Text.grid(row=4, column=0, padx=(10), pady=10)
        self.beforeVertex_Entry = Checkbutton(self.search_frame, variable=self.beforeVertex_Var)
        self.beforeVertex_Entry.grid(row=4, column=1, padx=(10), pady=10)


        self.startSearch_btn = Button(self.search_frame, text='Search', command = self.runSatelliteSearch)
        self.startSearch_btn.grid(row=5, column=1, padx=(10), pady=10)

        # gps initialization frame -----------------------------------------------
        self.gpsInfo_Frame = Frame(self.master_window)
        self.gpsInfo_Frame.pack(fill='y')

        self.gpsInfo_Label = Label(self.gpsInfo_Frame, text="GPS not set")
        self.gpsInfo_Label.grid(row=0, column=0, padx=(10), pady=10)

        # motor positions frame --------------------------------------------------------
        self.motorInfoFrame = Frame(self.master_window)
        self.motorInfoFrame.pack(fill='y')

        self.satInfo_Label = Label(self.motorInfoFrame, text="Satellite not selected")
        self.satInfo_Label.grid(row=0, column=0, padx=(10), pady=10)

        self.motorInfo_Label = Label(self.motorInfoFrame, text="Motors not initialized")
        self.motorInfo_Label.grid(row=1, column=0, padx=(10), pady=10)

        self.master_window.after(50, func=self.updateAppInfoFrame)

        self.master_window.mainloop()




    def runSatelliteSearch(self):
        satName = self.search_Entry.get() if self.search_Entry.get() != '' else None
        minElev = int(self.minElev_Entry.get()) if self.minElev_Entry.get() != '' else None
        maxWait = int(self.maxWait_Entry.get()) if self.maxWait_Entry.get() != '' else None

        search = satelliteSearch(observer = self.observer, satNameSearch = satName, minElevSearch = minElev, maxWaitSearch = maxWait)
        topResults = search.getTopResults()
        self.searchResultButtonPopulation(topResults)

    def searchResultButtonPopulation(self, topResults):
        try:
            temp = self.results_Frame
        except AttributeError:
            self.results_Frame = Frame(self.master_window)
            self.results_Frame.pack(fill='y')

        for widget in self.results_Frame.winfo_children():
            widget.destroy()
        rowCounter = 0
        for satResult in topResults:
            btn = Button(self.results_Frame, text=satResult.name, command= partial(self.resultClick, satResult))
            btn.grid(row=rowCounter, column=0)
            rowCounter = rowCounter + 1

    def resultClick(self, sat):
        self.motors.selectSatellite(sat)
        self.motors.setShouldTrack(True)
        try:
            temp = self.motorThread
        except AttributeError:
            self.motorThread = Thread(target=self.runAltAz)
            self.motorThread.daemon = True
            self.motorThread.start()

    def runAltAz(self):
        self.motors.driveMotors()

    def homeMotorsCommand(self):
        self.motors.setShouldHome(True)
        try:
            temp = self.motorThread
        except AttributeError:
            self.motorThread = Thread(target=self.runAltAz)
            self.motorThread.daemon = True
            self.motorThread.start()

    def alternateMotorState(self):
        if self.motors.enableState:
            self.btn_alternateMotorState['text'] = "Enable Motors"
        else:
            self.btn_alternateMotorState['text'] = "Disable Motors"
        self.motors.setEnableState(not self.motors.enableState)

    def setLocalization(self):
        self.latitude, self.longitude = gpsInterface.runGPS_Interface()
        self.observer.lat = self.latitude * ephem.degree
        self.observer.lon = self.longitude * ephem.degree
        self.observer.elev = 13
        self.observer.date = datetime.now(timezone.utc)
        print(self.latitude)
        print(self.longitude)
        self.motors.setObserver(self.observer)
        self.gpsInfo_Label['text'] = "Latitude = " + ((str)(self.latitude)) + "\nLongitude = " + ((str)(self.longitude))

    def updateAppInfoFrame(self):
        try:
            satElev =   round(self.motors.satellite.alt * toDeg, 2)
            satAz =     round(self.motors.satellite.az * toDeg, 2)
            motorElev = round(self.motors.currStepperElevation, 2)
            motorAz =   round(self.motors.currStepperAzimuth % 360, 2)
        except AttributeError:
            self.master_window.after(50, func=self.updateAppInfoFrame)
            return

        self.satInfo_Label['text'] =   "Satellite  : [Elev={0:.2f}, Az={1:.2f}]".format(satElev, satAz)
        self.motorInfo_Label['text'] = "Motors     : [Elev={0:.2f}, Az={1:.2f}]".format(motorElev, motorAz)
        self.master_window.after(50, func=self.updateAppInfoFrame)
    def Close(self):
        self.master_window.destroy()
        try:
            self.motors.endThread()
        except Exception:
            pass
        sleep(0.5)
        exit(0)



mainWindow()