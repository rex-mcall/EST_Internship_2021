from tkinter import *

master_window = Tk()
master_window.title("Satellite Tracker")
# master_window.attributes("-fullscreen", True)
master_window.state("zoomed")

# Parent widget for the buttons
buttons_frame = Frame(master_window)
buttons_frame.pack(fill='y')

btn_Disable = Button(buttons_frame, text='Disable Motors')
btn_Disable.grid(row=0, column=0, padx=(10), pady=10)

btn_Calibrate = Button(buttons_frame, text='Calibrate Sensors')
btn_Calibrate.grid(row=0, column=1, padx=(10), pady=10)

btn_Home = Button(buttons_frame, text='Home Motors')
btn_Home.grid(row=0, column=2, padx=(10), pady=10)

btn_Laser = Button(buttons_frame, text='Laser On/Off')
btn_Laser.grid(row=0, column=3, padx=(10), pady=10)

# Search Frame ----------------------------------------------------
search_frame = Frame(master_window)
search_frame.pack(fill='y')


search_Text = Label(search_frame, text="Satellite Name:")
search_Text.grid(row=0, column=0, padx=(10), pady=10)

search_Entry = Entry(search_frame)
search_Entry.grid(row=0, column=1, padx=(10), pady=10)



magnitudeFilter_Text = Label(search_frame, text="Minimum Magnitude:")
magnitudeFilter_Text.grid(row=1, column=0, padx=(10), pady=10)

magnitudeFilter_Entry = Entry(search_frame)
magnitudeFilter_Entry.grid(row=1, column=1, padx=(10), pady=10)



minElev_Text = Label(search_frame, text="Minimum Vertex Elevation (Deg):")
minElev_Text.grid(row=1, column=0, padx=(10), pady=10)

minElev_Entry = Entry(search_frame)
minElev_Entry.grid(row=1, column=1, padx=(10), pady=10)



maxWait_Text = Label(search_frame, text="Max Wait Till Rise (Mins):")
maxWait_Text.grid(row=2, column=0, padx=(10), pady=10)

maxWait_Entry = Entry(search_frame)
maxWait_Entry.grid(row=2, column=1, padx=(10), pady=10)



startSearch_btn = Button(search_frame, text='Search')
startSearch_btn.grid(row=3, column=1, padx=(10), pady=10)


mainloop()