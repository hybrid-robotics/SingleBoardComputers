#include <Wire.h>
#include "Adafruit_TCS34725.h"

/* Example code for the Adafruit TCS34725 breakout library */

/* Connect SCL    to analog 5
   Connect SDA    to analog 4
   Connect VDD    to 3.3V DC
   Connect GROUND to common ground */
   
/* Initialise with default values (int time = 2.4ms, gain = 1x) */
// Adafruit_TCS34725 tcs = Adafruit_TCS34725();

/* Initialise with specific int time and gain values */
Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_700MS, TCS34725_GAIN_1X);

#define  LED_PIN  2

void setup(void) {
  Serial.begin(115200);
  
  if (tcs.begin()) {
    Serial.println("Found sensor");
  } else {
    Serial.println("No TCS34725 found ... check your connections");
    while (1);
  }

  //  Set the LED pin to be an output
  pinMode(LED_PIN, OUTPUT);
  
  // Turn the LED off
  digitalWrite(LED_PIN, LOW);  
}

void loop(void) {
  uint16_t r, g, b, c, colorTemp, lux;
  
  tcs.getRawData(&r, &g, &b, &c);
  colorTemp = tcs.calculateColorTemperature(r, g, b);
  lux = tcs.calculateLux(r, g, b);
  
  Serial.print("Color Temp: ");
  Serial.print(colorTemp, DEC);
  Serial.print(" K, ");
  Serial.print("Lux: ");
  Serial.println(lux, DEC);
  
  Serial.print("Red: ");
  Serial.print(r, DEC);
  Serial.print(", ");
  Serial.print("Green: ");
  Serial.print(g, DEC);
  Serial.print(", ");
  Serial.print("Blue: ");
  Serial.println(b, DEC);

  Serial.print("C: ");
  Serial.println(c, DEC);
  Serial.println("");
}
