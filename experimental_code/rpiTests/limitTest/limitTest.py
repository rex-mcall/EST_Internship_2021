import RPi.GPIO as GPIO

elev_limit_pin = 11

GPIO.setup(elev_limit_pin, GPIO.IN)

while True:
    print(GPIO.input(elev_limit_pin))