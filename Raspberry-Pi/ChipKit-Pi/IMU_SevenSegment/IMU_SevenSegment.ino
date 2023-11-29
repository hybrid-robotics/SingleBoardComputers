#include <Adafruit_BMP085_U.h>
#include <Adafruit_GFX.h>

/*
  These are problems with ChipKit
*/
#include <RTClib.h>
#include <Adafruit_LEDBackpack.h>
#include <Adafruit_Sensor.h>

/*************************************************** 
  This is a library for our I2C LED Backpacks

  Designed specifically to work with the Adafruit LED 7-Segment backpacks 
  ----> http://www.adafruit.com/products/881
  ----> http://www.adafruit.com/products/880
  ----> http://www.adafruit.com/products/879
  ----> http://www.adafruit.com/products/878

  These displays use I2C to communicate, 2 pins are required to 
  interface. There are multiple selectable I2C addresses. For backpacks
  with 2 Address Select pins: 0x70, 0x71, 0x72 or 0x73. For backpacks
  with 3 Address Select pins: 0x70 thru 0x77

  Adafruit invests time and resources providing this open source code, 
  please support Adafruit and open-source hardware by purchasing 
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ****************************************************/

/****************************************************
  This sketch uses the 10DOF IMU from Adafruit, which has a
    BMP180 Temperature/Barometric pressure sensor, a
    LMS303 Three-axis accelerometer, and a
    L3GD20 Gyro
    
    Adafruit product http://www.adafruit.com/products/1604
*****************************************************/

// Enable one of these two #includes and comment out the other.
// Conditional #include doesn't work due to Arduino IDE shenanigans.
#include <Wire.h> // Enable this line if using Arduino Uno, Mega, etc.
//#include <TinyWireM.h> // Enable this line if using Adafruit Trinket, Gemma, etc.

Adafruit_7segment sevenSeg = Adafruit_7segment();
Adafruit_8x8matrix matrix8x8 = Adafruit_8x8matrix();

Adafruit_BMP085_Unified bmp = Adafruit_BMP085_Unified(10085);

void setup() {
#ifndef __AVR_ATtiny85__
  Serial.begin(115200);
#endif
  //  Initialize the 7-Segment display
  sevenSeg.begin(0x70);
  sevenSeg.setBrightness(1);
  
  matrix8x8.begin(0x71);
  matrix8x8.setBrightness(1);
  matrix8x8.setRotation(3);

  /* Initialise the BMP180 sensor */
  if(!bmp.begin()) {
    /* There was a problem detecting the BMP180 ... check your connections */
    Serial.print("Ooops, no BMP180 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
}

static const uint8_t PROGMEM
  hpa_bmp[] = {
    B10001110,
    B10001001,
    B11101110,
    B10101000,
    B00000100,
    B00001010,
    B00011111,
    B00010001
  },
    
  c_bmp[] = {
    B00111100,
    B01000010,
    B10000000,
    B10000000,
    B10000000,
    B10000000,
    B01000010,
    B00111100
  },
    
  f_bmp[] = {
    B11111110,
    B10000000,
    B10000000,
    B10000000,
    B11111000,
    B10000000,
    B10000000,
    B10000000
  },
    
  m_bmp[] = {
    B00000000,
    B00000000,
    B00000000,
    B00000000,
    B11111110,
    B10111010,
    B10010010,
    B10000010
  };

void loop() {
  float celsius, fahrenheit, altitude;
  float seaLevelPressure = SENSORS_PRESSURE_SEALEVELHPA;
  sensors_event_t event;

  /* Get a new sensor event */ 
  bmp.getEvent(&event);
  
  //  Display the barometric pressure in hPa
  if (event.pressure) {
    
    /* Calculating altitude with reasonable accuracy requires pressure    *
     * sea level pressure for your position at the moment the data is     *
     * converted, as well as the ambient temperature in degress           *
     * celcius.  If you don't have these values, a 'generic' value of     *
     * 1013.25 hPa can be used (defined as SENSORS_PRESSURE_SEALEVELHPA   *
     * in sensors.h), but this isn't ideal and will give variable         *
     * results from one day to the next.                                  *
     *                                                                    *
     * You can usually find the current SLP value by looking at weather   *
     * websites or from environmental information centers near any major  *
     * airport.                                                           *
     *                                                                    *
     * For example, for Paris, France you can check the current mean      *
     * pressure and sea level at: http://bit.ly/16Au8ol                   */

    //  First we get the current temperature from the BMP180 in celsius and fahrenheit
    bmp.getTemperature(&celsius);
    fahrenheit = (celsius * 1.8) + 32;

    //   Convert the atmospheric pressure, SLP and temp to altitude in meters
    altitude = bmp.pressureToAltitude(seaLevelPressure, event.pressure, celsius); 

    //  Display the barometric pressure in hPa
    sevenSeg.print(event.pressure);
    sevenSeg.writeDisplay();

    matrix8x8.clear();
    matrix8x8.drawBitmap(0, 0, hpa_bmp, 8, 8, LED_ON);
    matrix8x8.writeDisplay();

    delay(5000);

    //  Display the temperature in Celsius
    sevenSeg.print(celsius);
    sevenSeg.writeDisplay();

    matrix8x8.clear();
    matrix8x8.drawBitmap(0, 0, c_bmp, 8, 8, LED_ON);
    matrix8x8.writeDisplay();

    delay(5000);

    //  Display the temperature in Fahrenheit
    sevenSeg.print(fahrenheit);
    sevenSeg.writeDisplay();

    matrix8x8.clear();
    matrix8x8.drawBitmap(0, 0, f_bmp, 8, 8, LED_ON);
    matrix8x8.writeDisplay();

/*    
    delay(5000);
    
    //  Display altitude in meters
    sevenSeg.print(altitude);
    sevenSeg.writeDisplay();

    matrix8x8.clear();
    matrix8x8.drawBitmap(0, 0, m_bmp, 8, 8, LED_ON);
    matrix8x8.writeDisplay();

    for (int8_t x=7; x>=-36; x--) {
      matrix8x8.clear();
      matrix8x8.setCursor(x,0);
      matrix8x8.print("m");
      matrix8x8.writeDisplay();
      delay(100);
    }

    //  Display atmospheric pressue in hPa
    Serial.print("Pressure:    ");
    Serial.print(event.pressure);
    Serial.println(" hPa");
    
    //  Display the temperature in Celsius and Fahrenheit
    Serial.print("Temperature: ");
    Serial.print(celsius);
    Serial.print(" C, ");
    Serial.print(fahrenheit);
    Serial.println(" F");
    
    //  Display our altitude in meters
    Serial.print("Altitude:    ");
    Serial.print(altitude); 
    Serial.println(" m");
    Serial.println("");
*/

    delay(20000);
  }
}
