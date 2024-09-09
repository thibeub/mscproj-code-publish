/*
T. Atkins, 2024
> This is the script that runs on the ECM Arduino Uno and motor shield.
> The directory above this file is structured as such because it has been compiled as a PlatformIO project.
*/

#include <Arduino.h> // this inclusion is required when using PatformIO rather than the Arduino IDE

#define ENABLE_PIN A0 // pin that enables the motor shield when set HIGH

#define MOTOR_PIN 5
#define DIREC_PIN 6

// FWD_PIN and BACK_PIN are connected to each side of the SPDT switch in order to observe its state
#define FWD_PIN 13
#define BCK_PIN 10

int motorFastSpeed = 255; // 0-255 PWM value
int motorSlowSpeed = 150; // 0-255 PWM value

void setup() {
    Serial.begin(9600);

    // Setup pins
    pinMode(FWD_PIN, INPUT_PULLUP);
    pinMode(BCK_PIN, INPUT_PULLUP);

    pinMode(ENABLE_PIN, OUTPUT);

    pinMode(MOTOR_PIN, OUTPUT);
    pinMode(DIREC_PIN, OUTPUT);
}

void loop() {
    digitalWrite(ENABLE_PIN, HIGH); // enable the motor shield

    // Control the direction in which the motor spins based on the state of the SPDT switch
    if (digitalRead(FWD_PIN) == HIGH && digitalRead(BCK_PIN) == LOW) {
        digitalWrite(DIREC_PIN, HIGH);
        analogWrite(MOTOR_PIN, motorFastSpeed); // retract the cable (i.e. finger extension)
        // Serial.println("fwd");
    } else if (digitalRead(FWD_PIN) == LOW && digitalRead(BCK_PIN) == HIGH) {
        digitalWrite(DIREC_PIN, LOW);
        analogWrite(MOTOR_PIN, motorSlowSpeed); // release the cable (i.e. finger flexion) slowly
        // Serial.println("bck");
    } else {
        analogWrite(MOTOR_PIN, 0);
        // Serial.println("stop");
    }
}