from time import sleep
import RPi.GPIO as GPIO
import ephem
import datetime as dt
from datetime import datetime, timezone
from math import *
import re
import sys

# calculated constants to convert to and from radians
toDeg = 180 / pi
toRad = pi / 180

# elev motor driver pins
elev_dir_pin    = 21
elev_step_pin   = 20
elev_ms3_pin    = 26
elev_ms2_pin    = 19
elev_ms1_pin    = 13
elev_enable_pin =  6

# az motor driver pins
az_dir_pin    = 24
az_step_pin   = 23
az_ms3_pin    = 22
az_ms2_pin    = 27
az_ms1_pin    = 17
az_enable_pin =  4

# limit pins
elev_limit_pin = 11
az_limit_pin = 10



class motorInterface():
    def __init__(self, observer = None, satellite=None):
        self.satellite = satellite
        self.observer = observer

        # initializing stepper motor pins
        GPIO.setmode(GPIO.BCM)

        # setup elev motor pins
        GPIO.setup(elev_dir_pin, GPIO.OUT)
        GPIO.setup(elev_step_pin, GPIO.OUT)
        GPIO.setup(elev_ms3_pin, GPIO.OUT)
        GPIO.setup(elev_ms2_pin, GPIO.OUT)
        GPIO.setup(elev_ms1_pin, GPIO.OUT)
        GPIO.setup(elev_enable_pin, GPIO.OUT)

        #setup az motor pins
        GPIO.setup(az_dir_pin, GPIO.OUT)
        GPIO.setup(az_step_pin, GPIO.OUT)
        GPIO.setup(az_ms3_pin, GPIO.OUT)
        GPIO.setup(az_ms2_pin, GPIO.OUT)
        GPIO.setup(az_ms1_pin, GPIO.OUT)
        GPIO.setup(az_enable_pin, GPIO.OUT)

        # setup limit pins
        GPIO.setup(elev_limit_pin, GPIO.IN)
        GPIO.setup(az_limit_pin, GPIO.IN)

        self.stepMode_Elev = 8
        self.stepMode_Az = 8
        self.setMicrostepMode_Elev(self.stepMode_Elev)
        self.setMicrostepMode_Az(self.stepMode_Az)



        # initializes variables to remember the current angle of the azimuth and elevation
        self.currStepperAzimuth = 0
        self.currStepperElevation = 0

        # geared down ratios for degrees per step
        self.azDegPerStep = 0.36      # 1:5 ratio
        self.elevDegPerStep = 0.9     # 1:2 ratio

        # amount of time the step pulse is high and low
        self.stepDelay_Az = 0.0001
        self.stepDelay_Elev = 0.001

        self.keepTracking = False #inner loop of tracking thread
        self.keepHoming = False #inner loop of homing thread
        self.stopMotorsThread = False #exits the tracking thread when True
        self.stopHomingThread = False #exits the homing thread when True
        self.calibratedMotors = True #keeps track of whether the current recorded position of the motors is accurate
        self.enableState = False #keeps track of whether the motors are currently enabled

    def driveMotors(self):
        self.azHomed = False # initial homing with the sensor
        self.elevHomed = False
        self.azHomedRotate = False # rotation to correct position
        self.elevHomedRotate = False
        while not self.stopMotorsThread:
            if self.keepHoming:
                self.setShouldTrack(False) # stop trying to track a satellite while homing motors

                if not self.azHomed or not self.elevHomed or not self.azHomedRotate or not self.elevHomedRotate:
                    if not GPIO.input(az_limit_pin): # OPS is not interrupted and allows current flow
                        self.singleStep_Az(1)
                    else:
                        self.azHomed = True
                        self.currStepperAzimuth = 0
                    if self.azHomed and not self.azHomedRotate and self.currStepperAzimuth < 180:
                        self.setMicrostepMode_Az(16)
                        self.singleStep_Az(0)
                    else: 
                        self.azHomedRotate = True


                    if not GPIO.input(elev_limit_pin): # OPS is not interrupted and allows current flow
                        self.singleStep_Elev(0)
                    else:
                        self.elevHomed = True
                        self.currStepperElevation = 0
                    if self.elevHomed and not self.elevHomedRotate and self.currStepperElevation < 90:
                        self.setMicrostepMode_Elev(4)
                        self.singleStep_Az(0)
                    else: 
                        self.elevHomedRotate = True
                else:
                    self.setShouldHome(False)
                    self.calibratedMotors = True

            elif self.shouldTrack():
                    if self.stepMode_Az != 8:
                        self.setMicrostepMode_Az(8)
                    if self.stepMode_Elev != 8:
                        self.setMicrostepMode_Elev(8)

                    # refreshes the satellite position with the current time
                    self.observer.date = datetime.now(timezone.utc)
                    self.satellite.compute(self.observer)

                    # make sure satellite is above horizon, else reset motors to home position
                    if self.satellite.alt * toDeg > 0:

                        # calculates the angle to the correct elevation
                        elevErrDelta = (self.satellite.alt * toDeg) - self.currStepperElevation # <0 motor too high, >0 motor too low

                        # pulses the elevation stepper motor in the correct direction
                        if elevErrDelta >= (self.elevDegPerStep * 3/2):
                            self.singleStep_Elev(0)

                        elif elevErrDelta <= (-self.elevDegPerStep * 3/2):
                            self.singleStep_Elev(1)


                        # determines the most efficient direction to get to the correct azimuth
                        azErrDelta = 0
                        azMotorHomeAngle = self.satellite.az * toDeg
                        if abs((azMotorHomeAngle) - self.currStepperAzimuth) < abs(((azMotorHomeAngle) + 360) - self.currStepperAzimuth) and abs((azMotorHomeAngle) - self.currStepperAzimuth) < abs(((azMotorHomeAngle) - 360) - self.currStepperAzimuth):
                            azErrDelta = (self.satellite.az * toDeg) - self.currStepperAzimuth
                        elif abs(((azMotorHomeAngle) + 360) - self.currStepperAzimuth) < abs(((azMotorHomeAngle) - 360) - self.currStepperAzimuth):
                            azErrDelta = ((self.satellite.az * toDeg) + 360) - self.currStepperAzimuth
                        else:
                            azErrDelta = ((azMotorHomeAngle) - 360) - self.currStepperAzimuth

                        # pulses the azimuth stepper motor in the correct direction
                        if azErrDelta >= (self.azDegPerStep * 3/2):
                            self.singleStep_Az(1)

                        elif azErrDelta <= (-self.azDegPerStep * 3/2) :
                            self.singleStep_Az(0)


    # sets the microstep pins according to the input value
    # accepts the denominator of the step mode (1,2,4,8,16)
    def setMicrostepMode_Elev(self, stepMode):
        # MS1 MS2 MS3 Microstep Resolution Excitation Mode
        # L   L   L   Full Step            2 Phase
        # H   L   L   Half Step            1-2 Phase
        # L   H   L   Quarter Step         W1-2 Phase
        # H   H   L   Eighth Step          2W1-2 Phase
        # H   H   H   Sixteenth Step       4W1-2 Phase

        self.elevDegPerStep = 0.9  / stepMode  # 1:2 ratio
        self.stepMode_Elev = stepMode
        if stepMode == 1:
            GPIO.output(elev_ms3_pin, GPIO.LOW)
            GPIO.output(elev_ms2_pin, GPIO.LOW)
            GPIO.output(elev_ms1_pin, GPIO.LOW)

        elif stepMode == 2:
            GPIO.output(elev_ms3_pin, GPIO.LOW)
            GPIO.output(elev_ms2_pin, GPIO.LOW)
            GPIO.output(elev_ms1_pin, GPIO.HIGH)

        elif stepMode == 4:
            GPIO.output(elev_ms3_pin, GPIO.LOW)
            GPIO.output(elev_ms2_pin, GPIO.HIGH)
            GPIO.output(elev_ms1_pin, GPIO.LOW)

        elif stepMode == 8:
            GPIO.output(elev_ms3_pin, GPIO.HIGH)
            GPIO.output(elev_ms2_pin, GPIO.HIGH)
            GPIO.output(elev_ms1_pin, GPIO.LOW)

        elif stepMode == 16:
            GPIO.output(elev_ms3_pin, GPIO.HIGH)
            GPIO.output(elev_ms2_pin, GPIO.HIGH)
            GPIO.output(elev_ms1_pin, GPIO.HIGH)

    # sets the microstep pins according to the input value
    # accepts the denominator of the step mode (1,2,4,8,16)
    def setMicrostepMode_Az(self, stepMode):
        # MS1 MS2 MS3 Microstep Resolution Excitation Mode
        # L   L   L   Full Step            2 Phase
        # H   L   L   Half Step            1-2 Phase
        # L   H   L   Quarter Step         W1-2 Phase
        # H   H   L   Eighth Step          2W1-2 Phase
        # H   H   H   Sixteenth Step       4W1-2 Phase

        self.azDegPerStep   = 0.36 / stepMode  # 1:5 ratio
        self.stepMode_Az = stepMode
        if stepMode == 1:
            GPIO.output(az_ms3_pin, GPIO.LOW)
            GPIO.output(az_ms2_pin, GPIO.LOW)
            GPIO.output(az_ms1_pin, GPIO.LOW)

        elif stepMode == 2:
            GPIO.output(az_ms3_pin, GPIO.LOW)
            GPIO.output(az_ms2_pin, GPIO.LOW)
            GPIO.output(az_ms1_pin, GPIO.HIGH)

        elif stepMode == 4:
            GPIO.output(az_ms3_pin, GPIO.LOW)
            GPIO.output(az_ms2_pin, GPIO.HIGH)
            GPIO.output(az_ms1_pin, GPIO.LOW)

        elif stepMode == 8:
            GPIO.output(az_ms3_pin, GPIO.HIGH)
            GPIO.output(az_ms2_pin, GPIO.HIGH)
            GPIO.output(az_ms1_pin, GPIO.LOW)

        elif stepMode == 16:
            GPIO.output(az_ms3_pin, GPIO.HIGH)
            GPIO.output(az_ms2_pin, GPIO.HIGH)
            GPIO.output(az_ms1_pin, GPIO.HIGH)

    # defines how to drive the elevation stepper
    def singleStep_Elev(self, direction):
        if direction == 0:
            self.currStepperElevation = self.currStepperElevation + self.elevDegPerStep
        else:
            self.currStepperElevation = self.currStepperElevation - self.elevDegPerStep

        GPIO.output(elev_dir_pin, direction)
        GPIO.output(elev_step_pin, GPIO.HIGH)
        sleep(self.stepDelay_Elev)
        GPIO.output(elev_step_pin, GPIO.LOW)
        sleep(self.stepDelay_Elev)

    # defines how to drive the azimuth stepper
    def singleStep_Az(self, direction):
        if direction == 0:
            self.currStepperAzimuth = self.currStepperAzimuth - self.azDegPerStep
        else:
            self.currStepperAzimuth = self.currStepperAzimuth + self.azDegPerStep
        GPIO.output(az_dir_pin, direction)
        GPIO.output(az_step_pin, GPIO.HIGH)
        sleep(self.stepDelay_Az)
        GPIO.output(az_step_pin, GPIO.LOW)
        sleep(self.stepDelay_Az)

    # turns the enable pin on or off for both stepper motors
    # mainly used during compass calibration to reduce electromagnetic interference
    def setEnableState(self, state):
        if state:
            GPIO.output(elev_enable_pin, GPIO.LOW)
            GPIO.output(az_enable_pin, GPIO.LOW)
            self.enableState = True
        else:
            GPIO.output(elev_enable_pin, GPIO.HIGH)
            GPIO.output(az_enable_pin, GPIO.HIGH)
            self.calibratedMotors = False
            self.enableState = False

    def selectSatellite(self, newSatellite):
        self.satellite = newSatellite

    def setObserver(self, newObserver):
        self.observer = newObserver

    def setShouldTrack(self, trackBool):
        self.keepTracking = trackBool

    def setShouldHome(self, homeBool):
        self.keepHoming = homeBool
        if homeBool:
            self.azHomed = False
            self.elevHomed = False
            self.azHomedRotate = False
            self.elevHomedRotate = False

    def shouldTrack(self):
        if self.keepTracking and self.calibratedMotors and self.satellite != None and self.observer != None:
            return True
        else:
            return False

    def endThread(self):
        self.stopMotorsThread = True
        self.stopHomingThread = True
        sleep(1)
        self.cleanupGPIO()

    def cleanupGPIO(self):
        GPIO.cleanup()