/*
T. Atkins, 2024
> This Arduino script is used to determine the calibration factor that should be applied to the readout of the cantilever load cells (which provide data amplified by an HX711 module before being reeived by the Arduino).
> Elements of the code below are also found in tsf/tsf_tx/tsf_tx.ino - a script that is used to transmit load cell readings from the T-SF test rig over serial.
> This code is MODIFIED from that provided for Sparkfun amplifiers by N. Seidle et al. (https://github.com/sparkfun/HX711-Load-Cell-Amplifier).
*/

#include "HX711.h"

// Pins for load cell A (LC-A)
// #define DOUT  3
// #define CLK  2

// Pins for load cell B (LC-B)
#define DOUT  7
#define CLK  6

HX711 scale;

// float calibration_factor = -210000; // calibration factor for LC-A (tuned with a 0.1 kg calibration weight)
float calibration_factor = 210000; // calibration factor for LC-B

void setup() {
  Serial.begin(9600);
  Serial.println("HX711 load cell (LC) calibration sketch.");
  Serial.println("Remove all weight from the LC.");
  Serial.println("After readings begin, place known weight on the LC.");

  scale.begin(DOUT, CLK);
  scale.set_scale();
  scale.tare(); // reset the scale to 0

  long zero_factor = scale.read_average(); // retrieve a baseline reading
  Serial.print("Zero factor: "); // can be used to remove the need to tare the scale
  Serial.println(zero_factor);
}

void loop() {
  scale.set_scale(calibration_factor);

  Serial.print("Reading: ");
  Serial.print(scale.get_units(), 4);
  Serial.print(" kg");
  Serial.print(" calibration_factor: ");
  Serial.print(calibration_factor);
  Serial.println();
}