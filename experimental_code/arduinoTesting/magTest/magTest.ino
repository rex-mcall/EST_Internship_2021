#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>

/* Assign a unique ID to this sensor at the same time */
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(1);

void setup(void)
{
    Serial.begin(9600);

    /* Initialise the sensor */
    if (!mag.begin())
    {
        /* There was a problem detecting the HMC5883 ... check your connections */
        Serial.println("Ooops, no HMC5883 detected ... Check your wiring!");
        while (1)
            ;
    }
}

double getHeadingDegrees(Adafruit_HMC5883_Unified magInstance)
{
    /* Get a new sensor event */
    sensors_event_t event;
    magInstance.getEvent(&event);

    // Hold the module so that Z is pointing 'up' and you can measure the heading with x&y
    // Calculate heading when the magnetometer is level, then correct for signs of axis.
    float heading = atan2(event.magnetic.x, event.magnetic.y);

    float declinationAngle = -0.193;
    heading += declinationAngle;

    // Correct for when signs are reversed.
    if (heading < 0)
        heading += 2 * PI;

    // Check for wrap due to addition of declination.
    if (heading > 2 * PI)
        heading -= 2 * PI;

    // Convert radians to degrees for readability.
    float headingDegrees = heading * 180 / M_PI;

    return headingDegrees;
}

void loop(void)
{
    Serial.println(getHeadingDegrees(mag));
    delay(250);
}