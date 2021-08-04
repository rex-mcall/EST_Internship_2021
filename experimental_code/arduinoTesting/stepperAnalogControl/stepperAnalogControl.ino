const int step = 10;
const int dir  =  9;

const int ms1  =  2;
const int ms2  =  3;
const int ms3  =  4;

const int joyX = A0;

void setup() {
    pinMode(step, OUTPUT);
    pinMode(dir, OUTPUT);

    pinMode(ms1, OUTPUT);
    pinMode(ms2, OUTPUT);
    pinMode(ms3, OUTPUT);

    pinMode(joyX, INPUT);

    //full step mode
    digitalWrite(ms1, LOW);
    digitalWrite(ms2, LOW);
    digitalWrite(ms3, LOW);
}

void loop() {
    int joyXVal = analogRead(joyX) - 512;

    int xStepPerSec = abs(int((double(joyXVal) * 11.719) / 60.0));

    int xStepDelay = int((1.0 / double(xStepPerSec)) / 2.0);

    if (joyXVal >=  10) {
        digitalWrite(dir, HIGH);

        digitalWrite(step, HIGH);
        delayMicroseconds(xStepDelay);
        digitalWrite(step, LOW);
        delayMicroseconds(xStepDelay);
    }
    else if (joyXVal <= -10) {
        digitalWrite(dir, LOW);

        digitalWrite(step, HIGH);
        delayMicroseconds(xStepDelay);
        digitalWrite(step, LOW);
        delayMicroseconds(xStepDelay);
    }

}