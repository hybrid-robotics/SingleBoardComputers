#include <Boards.h>
#include <Adafruit_Sensor.h>
//#include <Adafruit_BMP180_Unified.h>
#include <RTClib.h>

/*
  SensorPeripheral
  Acts as a peripheral to a host computer to read sensors.
  
  Credit is given, where applicable, for code I did not write.
 
  Copyright (C) 2013 Dale Weber <hybotics.pdx@gmail.com>.
 */
 
// Pin 13 has an LED connected on most Arduino boards.
// Give it a name:
#define  HEARTBEAT_LED     13
#define  ANALOG_BASE       14
#define  DIGITAL_BASE       2

#define  MAX_PING           1
#define  MAX_GP2D12         2

int analogPin = 0;
int digitalPin = 0;
int digitalBase = 2;

int ping[MAX_PING];

float gp2d12[MAX_GP2D12];

/* 
 read_gp2d12_range
 Function that reads a value from GP2D12 infrared distance sensor and returns a value in centimeters.

 This sensor should be used with a refresh rate of 36ms or greater.

 Javier Valencia 2008

 float read_gp2d12_range(byte pin)

 It can return -1 if something gone wrong.

*/
float read_gp2d12 (byte pin) {
  int tmp;

  tmp = analogRead(pin);

  if (tmp < 3)
    return -1;                                  // Invalid value
  else
    return (6787.0 /((float)tmp - 3.0)) - 4.0;  // Distance in cm
} 

long microsecondsToInches(long microseconds) {
  // According to Parallax's datasheet for the PING))), there are
  // 73.746 microseconds per inch (i.e. sound travels at 1130 feet per
  // second).  This gives the distance travelled by the ping, outbound
  // and return, so we divide by 2 to get the distance of the obstacle.
  // See: http://www.parallax.com/dl/docs/prod/acc/28015-PING-v1.3.pdf
  return microseconds / 74 / 2;
}

long microsecondsToCentimeters(long microseconds) {
  // The speed of sound is 340 m/s or 29 microseconds per centimeter.
  // The ping travels out and back, so to find the distance of the
  // object we take half of the distance travelled.
  return microseconds / 29 / 2;
}

/* Ping))) Sensor
 
   This sketch reads a PING))) ultrasonic rangefinder and returns the
   distance to the closest object in range. To do this, it sends a pulse
   to the sensor to initiate a reading, then listens for a pulse
   to return.  The length of the returning pulse is proportional to
   the distance of the object from the sensor.
     
   The circuit:
    * +V connection of the PING))) attached to +5V
    * GND connection of the PING))) attached to ground
    * SIG connection of the PING))) attached to digital pin 7

   http://www.arduino.cc/en/Tutorial/Ping
   
   Created 3 Nov 2008
   by David A. Mellis
 
   Modified 30-Aug-2011
   by Tom Igoe

   Modified 09-Aug-2013
   by Dale Weber
 
   This example code is in the public domain.
*/

// Set units = true for inches and false for cm
int readPing (byte pingPin, boolean units) {
  // establish variables for duration of the ping,
  // and the distance result in inches and centimeters:
  long duration;
  int result;

  // The PING))) is triggered by a HIGH pulse of 2 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  pinMode(pingPin, OUTPUT);
  digitalWrite(pingPin, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(pingPin, LOW);

  // The same pin is used to read the signal from the PING))): a HIGH
  // pulse whose duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  pinMode(pingPin, INPUT);
  duration = pulseIn(pingPin, HIGH);

  // Convert the time into a distance
  if (units) {
    // Return result in inches.
    result = microsecondsToInches(duration);
  } else {
    // Return result in cm
    result = microsecondsToCentimeters(duration);
  }
 
  delay(100);
  
  return result;
}

void pulseDigital(int pin, int duration) {
  digitalWrite(pin, HIGH);   // Turn the ON by making the voltage HIGH (5V)
  delay(duration);           // Wait for duration ms
  digitalWrite(pin, LOW);    // Turn the pin OFF by making the voltage LOW (0V)
  delay(duration);           // Wait for duration ms
}

// The setup routine runs once when you press reset:
void setup() {                
  Serial.begin(115200);
 // initialize the digital pin as an output.
  pinMode(HEARTBEAT_LED, OUTPUT);
  
  for (analogPin = 0; analogPin < 5; analogPin++) {
    pinMode(analogPin + ANALOG_BASE, INPUT);
  }
}

// The loop routine runs forever:
void loop() {
  // Pulse the heartbeat LED
  pulseDigital(HEARTBEAT_LED, 500);

  // Read the GP2D12 Analog IR sensors and store the readings  
  for (analogPin = 0; analogPin < MAX_GP2D12; analogPin++) { 
    gp2d12[analogPin] = read_gp2d12(analogPin);
  }

  // Display the GP2D12 sensor readings (cm)
  for (analogPin = 0; analogPin < MAX_GP2D12; analogPin++) { 
    Serial.print("gp2d12 #");
    Serial.print(analogPin + 1);
    Serial.print(" range = ");
    Serial.print(gp2d12[analogPin]);
    Serial.println(" cm");
  }  
  
  Serial.println("");
  
  // Read PING Ultrasonic sensors
  for (digitalPin = 0; digitalPin < MAX_PING; digitalPin++) {
    ping[digitalPin] = readPing(digitalPin + DIGITAL_BASE, false);
  }
  
  // Display PING sensor readings (cm)
  for (digitalPin = 0; digitalPin < MAX_PING; digitalPin++) {
    Serial.print("Ping #");
    Serial.print(digitalPin + 1);
    Serial.print(" range = ");
    Serial.print(ping[digitalPin]);
    Serial.println(" cm");
  }
  
  Serial.println("");
  
  delay(200);
}
