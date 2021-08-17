from tkinter import *
import ephem
import datetime as dt
from datetime import datetime, timezone
from math import *
from satelliteCalculations import satelliteSearch

class mainWindow():
    def __init__(self):
        self.master_window = Tk()
        self.master_window.title("Satellite Tracker")
        self.master_window.attributes("-fullscreen", True)
        # self.master_window.state("zoomed")

        # Top Buttons Frame ----------------------------------------------------
        self.buttons_frame = Frame(self.master_window)
        self.buttons_frame.pack(fill='y')

        self.btn_Disable = Button(self.buttons_frame, text='Disable Motors')
        self.btn_Disable.grid(row=0, column=0, padx=(10), pady=10)

        self.btn_Calibrate = Button(self.buttons_frame, text='Calibrate Sensors')
        self.btn_Calibrate.grid(row=0, column=1, padx=(10), pady=10)

        self.btn_Home = Button(self.buttons_frame, text='Home Motors')
        self.btn_Home.grid(row=0, column=2, padx=(10), pady=10)

        self.btn_Laser = Button(self.buttons_frame, text='Laser On/Off')
        self.btn_Laser.grid(row=0, column=3, padx=(10), pady=10)

        self.btn_switchWindow = Button(self.buttons_frame, text='Switch to Tracking Page', command=self.switchWindow)
        self.btn_switchWindow.grid(row=0, column=4, padx = 10, pady = 10)

        self.btn_closeApp = Button(self.buttons_frame, text='Exit Application', command=self.Close)
        self.btn_closeApp.grid(row=0, column=5, padx = 10, pady = 10)

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

        self.magnitudeFilter_Text = Label(self.search_frame, text="Minimum Magnitude:")
        self.magnitudeFilter_Text.grid(row=3, column=0, padx=(10), pady=10)
        self.magnitudeFilter_Entry = Entry(self.search_frame)
        self.magnitudeFilter_Entry.grid(row=3, column=1, padx=(10), pady=10)


        self.startSearch_btn = Button(self.search_frame, text='Search', command = self.runSatelliteSearch)
        self.startSearch_btn.grid(row=4, column=1, padx=(10), pady=10)

        self.master_window.mainloop()

    def runSatelliteSearch(self):
        satName = self.search_Entry.get() if self.search_Entry.get() != '' else None
        minElev = int(self.minElev_Entry.get()) if self.minElev_Entry.get() != '' else None
        maxWait = dt.timedelta(minutes=int(self.maxWait_Entry.get())) if self.maxWait_Entry.get() != '' else None
        minMagnitude = int(self.magnitudeFilter_Entry.get()) if self.magnitudeFilter_Entry.get() != '' else None

        search = satelliteSearch(satNameSearch = satName, minElevSearch = minElev, maxWaitSearch = maxWait, minMagSearch = minMagnitude)
        top5Results = search.getTop5Results()
        self.searchResultButtonPopulation(top5Results)

    def searchResultButtonPopulation(self, top5Results):
        self.results_Frame = Frame(self.master_window)
        self.results_Frame.pack(fill='y')

        rowCounter = 0
        for satResult in top5Results:
            btn = Button(self.results_Frame, text=satResult.name)
            btn.grid(row=rowCounter, column=0)
            rowCounter = rowCounter + 1

    def switchWindow(self):
        self.master_window.destroy()
        infoWindow()
    def Close(self):
        self.master_window.destroy()

class infoWindow():
    def __init__(self):
        self.master_window = Tk()
        self.master_window.title("Satellite Tracker")
        self.master_window.attributes("-fullscreen", True)

        # buttons bar -----------------------------------------------
        buttons_frame = Frame(self.master_window)
        buttons_frame.pack(fill='y')

        btn_Disable = Button(buttons_frame, text='Disable Motors')
        btn_Disable.grid(row=0, column=0, padx=(10), pady=10)

        btn_Calibrate = Button(buttons_frame, text='Calibrate Sensors')
        btn_Calibrate.grid(row=0, column=1, padx=(10), pady=10)

        btn_Home = Button(buttons_frame, text='Home Motors')
        btn_Home.grid(row=0, column=2, padx=(10), pady=10)

        btn_Laser = Button(buttons_frame, text='Laser On/Off')
        btn_Laser.grid(row=0, column=3, padx=(10), pady=10)

        btn_switchWindow = Button(buttons_frame, text='Switch to Search Page', command=self.switchWindow)
        btn_switchWindow.grid(row=0, column=4, padx = 10, pady = 10)

        btn_closeApp = Button(buttons_frame, text='Exit Application', command=self.Close)
        btn_closeApp.grid(row=0, column=5, padx = 10, pady = 10)

    def switchWindow(self):
        self.master_window.destroy()
        mainWindow()
    def Close(self):
        self.master_window.destroy()



mainWindow()