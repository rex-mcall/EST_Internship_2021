const int step = 10;
const int dir  =  9;

const int ms1  =  2;
const int ms2  =  3;
const int ms3  =  4;

const int joyX = A0;

int maxRPM = 45;
double scaleTerm = ((maxRPM * 200.0) / 512.0)/60.0;

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
    Serial.begin(9600);
}

void loop() {
    int joyXVal = analogRead(joyX) - 512;

    double xStepPerSec = abs(joyXVal) * scaleTerm;

    long xStepDelayMS = long(((1.0 / xStepPerSec) / 2.0) * 100000);


    if (joyXVal >=  -3) {
        digitalWrite(dir, HIGH);

        digitalWrite(step, HIGH);
        delayMicroseconds(xStepDelayMS);
        digitalWrite(step, LOW);
        delayMicroseconds(xStepDelayMS);
    }
    else if (joyXVal <= -23) {
        digitalWrite(dir, LOW);

        digitalWrite(step, HIGH);
        delayMicroseconds(xStepDelayMS);
        digitalWrite(step, LOW);
        delayMicroseconds(xStepDelayMS);
    }

}