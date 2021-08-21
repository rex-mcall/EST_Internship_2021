from time import sleep
import RPi.GPIO as GPIO

DIR = 20   # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 400 * 4   # Steps per Revolution (360 / 1.8)

secondsPerRev = 8
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

# MS1 MS2 MS3 Microstep Resolution Excitation Mode
# L   L   L   Full Step            2 Phase
# H   L   L   Half Step            1-2 Phase
# L   H   L   Quarter Step         W1-2 Phase
# H   H   L   Eighth Step          2W1-2 Phase
# H   H   H   Sixteenth Step       4W1-2 Phase

GPIO.output(elev_ms3_pin, GPIO.LOW)
GPIO.output(elev_ms2_pin, GPIO.HIGH)
GPIO.output(elev_ms1_pin, GPIO.HIGH)
GPIO.output(elev_enable_pin, GPIO.LOW) # Active low to enable motor outputs

GPIO.output(az_ms3_pin, GPIO.LOW)
GPIO.output(az_ms2_pin, GPIO.HIGH)
GPIO.output(az_ms1_pin, GPIO.HIGH)
GPIO.output(az_enable_pin, GPIO.LOW) # Active low to enable motor outputs

step_count = SPR
delay = 0.001

for x in range(step_count):
    GPIO.output(elev_step_pin, GPIO.HIGH)
    sleep(delay)
    GPIO.output(elev_step_pin, GPIO.LOW)
    sleep(delay)

sleep(.5)
GPIO.output(DIR, CCW)
for x in range(step_count):
    GPIO.output(elev_step_pin, GPIO.HIGH)
    sleep(delay)
    GPIO.output(elev_step_pin, GPIO.LOW)
    sleep(delay)

GPIO.cleanup()