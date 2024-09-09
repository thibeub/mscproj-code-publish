#include "HX711.h"

// Command pins
#define REC_PIN 4 // pressing this button indicates to the Python script that it should record the load cell readings
#define STOP_PIN 9 // pressing this button saves test data as a CSV and stops execution on the Python side.

// Pins for LC-A (used for T-TF)
// #define DOUT 3
// #define CLK 2

// Pins for LC-B (used for T-SF)
#define DOUT  7
#define CLK  6

HX711 scale;

// float calibration_factor = -212100;  // for LC-A
float calibration_factor = 210000; // for LC-B

void setup() {
  Serial.begin(9600);

  // Setup command pins
  pinMode(REC_PIN, INPUT_PULLUP);
  pinMode(STOP_PIN, INPUT_PULLUP);

  // LC setup
  scale.begin(DOUT, CLK);
  scale.set_scale();
  scale.tare();  // reset the scale to 0
  scale.set_gain(128);
}

void loop() {
  scale.set_scale(calibration_factor);

  if (digitalRead(REC_PIN) == LOW && digitalRead(STOP_PIN) == HIGH) { // RECORD
    Serial.println(1000); // this is the 'RECORD' code: load measured will not approach 1000 kg, so this is a code (saves in complexity versus sensing both numerical and string data over serial to Python and parsing it)
    delay(2000);
  } else if (digitalRead(REC_PIN) == HIGH && digitalRead(STOP_PIN) == LOW) { // STOP
    Serial.println(2000); // as above, this is the 'STOP' code
    delay(2000);
  } else {
    Serial.println(scale.get_units(), 5);
  }
}