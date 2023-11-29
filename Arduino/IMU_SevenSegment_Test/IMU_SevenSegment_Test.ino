#include <Adafruit_Sensor.h>
#include <Adafruit_BMP180_Unified.h>
#include <Adafruit_GFX.h>
#include <Adafruit_LEDBackpack.h>
#include <RTClib.h>

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

Adafruit_BMP180_Unified bmp180 = Adafruit_BMP180_Unified(10085);
RTC_DS1307 rtc;

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
    B01110000,
    B10001000,
    B10000000,
    B10001000,
    B01110000,
    B00000000,
    B00000000,
    B00000000
  },
    
  f_bmp[] = {
    B11111000,
    B10000000,
    B11100000,
    B10000000,
    B10000000,
    B00000000,
    B00000000,
    B00000000
  },
    
  m_bmp[] = {
    B00000000,
    B00000000,
    B00000000,
    B00000000,
    B11101110,
    B10111010,
    B10010010,
    B10000010
  },
  
  am_bmp[] = {
    B01110000,
    B10001010,
    B10001010,
    B01110100,
    B00110110,
    B01001001,
    B01001001,
    B01001001
  },
 
  pm_bmp[] = {
    B01111100,
    B10000010,
    B11111100,
    B10000000,
    B10110110,
    B01001001,
    B01001001,
    B01001001
  };

String padString (String st, uint8_t nrPlaces) {
  uint8_t i, len;
  String newString = st;
  
  if (newString.length() < nrPlaces) {
    len = st.length();
  
    for (i = len; i < nrPlaces; i++) {
      newString = String("0" + newString);
    }
  }

  return newString;
}

float tempFahrenheit (float celsius) {
  return (celsius * 1.8) + 32;
}

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
  if(!bmp180.begin()) {
    /* There was a problem detecting the BMP180 ... check your connections */
    Serial.print("Ooops, no BMP180 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
}

void loop() {
  boolean amTime;
  DateTime now = rtc.now();
  float celsius, fahrenheit, altitude;
  float seaLevelPressure = SENSORS_PRESSURE_SEALEVELHPA;
  sensors_event_t event;
  
  uint8_t hour = now.hour();
  uint16_t timeInt;

  String timeString;
  String currMonth = padString(String(now.month()), 2);
  String currDay = padString(String(now.day()), 2);
  String currYear = padString(String(now.year()), 4);
  String currHour;
  String currMinute = padString(String(now.minute()), 2);
  String currSecond = padString(String(now.second()), 2);

  Serial.print("Hour = ");
  Serial.println(hour);
 
  if (hour > 12) {
    amTime = false;
    hour = hour - 12;
  } else {
    amTime = true;
  }

  timeInt = (hour * 100) + now.minute();  
  timeString = padString(String((hour * 100) + now.minute()), 4);
  currHour = padString(String(hour), 2);

  //  Display the current time on the 7 segment display
  sevenSeg.print(timeInt);
  sevenSeg.drawColon(true);
  
  matrix8x8.clear();
  
  if (amTime) {
    matrix8x8.drawBitmap(0, 0, am_bmp, 8, 8, LED_ON);
  } else {
    matrix8x8.drawBitmap(0, 0, pm_bmp, 8, 8, LED_ON);
  }
  
  sevenSeg.writeDisplay();
  matrix8x8.writeDisplay();
  
  delay(45000);

/*
  //  Display the current time
  Serial.print("Current date: ");
  Serial.print(currMonth);
  Serial.print('/');
  Serial.print(currDay);
  Serial.print('/');
  Serial.println(currYear);
  
  Serial.print("Current time: (");
  Serial.print(timeString);
  Serial.print(") ");
  Serial.print(currHour);
  Serial.print(':');
  Serial.print(currMinute);
  Serial.print(':');
  Serial.print(currSecond);
  Serial.print(" ");
  Serial.println(amPM);
  Serial.println();
*/

  /* Get a new sensor event */ 
  bmp180.getEvent(&event);
  
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
    bmp180.getTemperature(&celsius);
    fahrenheit = tempFahrenheit(celsius);

    //   Convert the atmospheric pressure, SLP and temp to altitude in meters
    altitude = bmp180.pressureToAltitude(seaLevelPressure, event.pressure, celsius); 
/*
    //  Display the barometric pressure in hPa
    sevenSeg.print(event.pressure);
    sevenSeg.writeDisplay();

    matrix8x8.clear();
    matrix8x8.drawBitmap(0, 0, hpa_bmp, 8, 8, LED_ON);
    matrix8x8.writeDisplay();

    delay(5000);
*/
    //  Display the temperature in Celsius
    sevenSeg.print(celsius);
    sevenSeg.writeDisplay();

    matrix8x8.clear();
    matrix8x8.drawBitmap(0, 0, c_bmp, 8, 8, LED_ON);
    matrix8x8.writeDisplay();

    delay(7500);

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
    Serial.println();
    delay(7500);
  }
}
