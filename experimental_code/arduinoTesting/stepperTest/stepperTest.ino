const int dirPin = 10;
const int stepPin = 9;
const int stepsPerRevolution = 200;

const int potX = 7;
const int potY = 8;

void setup()
{
    // Declare pins as Outputs
    pinMode(stepPin, OUTPUT);
    pinMode(dirPin, OUTPUT);
}
void loop()
{
    // Set motor direction clockwise
    digitalWrite(dirPin, HIGH);

    // Spin motor slowly
    for (int x = 0; x < stepsPerRevolution; x++)
    {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(2000);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(2000);
    }
    delay(1000); // Wait a second

    // Set motor direction counterclockwise
    digitalWrite(dirPin, LOW);

    // Spin motor quickly
    for (int x = 0; x < stepsPerRevolution; x++)
    {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(1000);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(1000);
    }
    delay(1000); // Wait a second
}
