/*
  Program:      W.A.L.T.E.R. 2.0, Main navigation and reactive behaviors
  Date:         29-Dec-2013
  Version:      0.1.2 ALPHA

  Purpose:      Added new displaySoundDirection() routine. I've started to add some
                  error handling code, as well as code to handle Wire (I2C) slave
                  operation.
                  
                Connected BotBoarduino to SSC-32, and they communicate fine. Added a
                  nice little moveServoPw() and moveServoDegrees() routines that
                  include speed and time parameters. Added servo move routines,
                  sensor display routines, modified the servo structure to include
                  max degrees (90 or 180), so the appropriate value can ge stored
                  in servo.angle for each servo. The servo move routines support
                  combination moves.

  Dependencies: Adafruit libraries:
                  LSM303DLHC, L3GD20, TMP006, TCS34727, RTClib for the DS1307  

                Hybotics libraries:
                  BMP180 (modified from Adafruit's BMP085 library)
                  
  Comments:     Credit is given, where applicable, for code I did not originate.
                  This sketch started out as an Adafruit tutorial for the electret
                  microphones being used for sound detection. I've also pulled
                  code for the GP2D12 IR and PING sensors from the Arduino
                  Playground, which I have modified to suit my needs.
 
                Copyright (C) 2013 Dale Weber <hybotics.pdx@gmail.com>.
*/

#include <Wire.h>

#include <Adafruit_Sensor.h>

#include <Adafruit_BMP180_Unified.h>
#include <Adafruit_LSM303DLHC_Unified.h>
#include <Adafruit_L3GD20.h>

#include <Adafruit_TCS34725.h>
#include <Adafruit_TMP006.h>
#include <RTClib.h>

#include "Walter.h"

/*
    Initialize our sensors
    
    We have:
      These are all on a single small board from Adafruit
        http://www.adafruit.com/products/1604
        A BMP180 temperature and pressure sensor
        An L3GD20 Gyro
        An LSM303 3-Axis accelerometer / magnetometer (compass)
      
      These are also from Adafruit:
        http://www.adafruit.com/products/1334 (TCS34725 RGB Color sensor)
        http://www.adafruit.com/products/1296 (TMP006 Heat sensor)
        http://www.adafruit.com/products/264 (DS1307 Realtime Clock)
      
      GP2D12 IR Ranging sensors (3)
      PING Ultrasonic Ranging sensors (3)
*/

Adafruit_BMP180_Unified temperature = Adafruit_BMP180_Unified(10001);
Adafruit_L3GD20 gyro;
Adafruit_LSM303_Accel_Unified accelerometer = Adafruit_LSM303_Accel_Unified(10002);
Adafruit_LSM303_Mag_Unified magnetometer = Adafruit_LSM303_Mag_Unified(10003);

Adafruit_TCS34725 color = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_50MS, TCS34725_GAIN_4X);
Adafruit_TMP006 heat;
RTC_DS1307 ds1307;

/*
    Initialize global variables
*/

//  Storage for sound detection sample data
Sample samples[MAX_SAMPLES];

/*
    Initialize servos
*/
Servo panServo = {
  SERVO_PAN_PIN,
  SERVO_PAN_ADJUST,
  0,
  0,
  SERVO_PAN_LEFT_MAX,
  SERVO_PAN_RIGHT_MAX,
  SERVO_MAX_DEGREES,
  0
};

Servo tiltServo = {
  SERVO_TILT_PIN,
  SERVO_TILT_ADJUST,
  0,
  0,
  SERVO_TILT_DOWN_MAX,
  SERVO_TILT_UP_MAX,
  SERVO_MAX_DEGREES,
  0
};

//  These are where the sensor readings are stored.
int ping[MAX_PING];
float gp2d12[MAX_GP2D12];

/****************************************************************
                          Code starts here
*****************************************************************/

/*
    Display the GP2D12 sensor readings (cm)
*/
void displayGP2D12 (void) {
  int sensorNr;
  
  for (sensorNr = 0; sensorNr < MAX_GP2D12; sensorNr++) { 
    Serial.print("gp2d12 #");
    Serial.print(sensorNr + 1);
    Serial.print(" range = ");
    Serial.print(gp2d12[sensorNr]);
    Serial.println(" cm");
  }  
  
  Serial.println("");  
}

/* 
    Function that reads a value from GP2D12 infrared distance sensor and returns a
      value in centimeters.

    This sensor should be used with a refresh rate of 36ms or greater.

    Javier Valencia 2008

    float read_gp2d12(byte pin)

    It can return -1 if something gone wrong.
    
    TODO: Make several readings over a time period, and average them
      for the final reading.
*/
float readGP2D12 (byte pin) {
  int tmp;

  tmp = analogRead(pin);

  if (tmp < 3)
    return -1;                                  // Invalid value
  else
    return (6787.0 /((float)tmp - 3.0)) - 4.0;  // Distance in cm
} 

float readGP2D12b (byte pin) {
  int reading, sampleCount;
  int readingMin = 1024, readingMax = 0, readingAdustment = 0, finalReading = 0;
  float value = 0.0;

  for (sampleCount = 0; sampleCount < MAX_IR_SAMPLES; sampleCount++) {    
    reading = analogRead(pin);

    if (reading >= 3) {
      if (value >= readingMax) {
        readingMax = reading;
      } else if (reading <= readingMin) {
        readingMin = reading;
      }
    } else {
      reading = -1;
    }
    
    delay(2);
  }

  readingAdustment = (readingMax - readingMin) / MAX_IR_SAMPLES;
  finalReading = ((readingMax + readingMin) / 2) + readingAdustment;

  value = (6787.0 / ((float)finalReading - 3.0)) - 4.0;  // Distance in cm

  return value;
}
/*
    Convert a pulse width in ms to inches
*/
long microsecondsToInches(long microseconds) {
  // According to Parallax's datasheet for the PING))), there are
  // 73.746 microseconds per inch (i.e. sound travels at 1130 feet per
  // second).  This gives the distance travelled by the ping, outbound
  // and return, so we divide by 2 to get the distance of the obstacle.
  // See: http://www.parallax.com/dl/docs/prod/acc/28015-PING-v1.3.pdf
  return microseconds / 74 / 2;
}

/*
    Convert a pulse width in ms to a distance in cm
*/
long microsecondsToCentimeters(long microseconds) {
  // The speed of sound is 340 m/s or 29 microseconds per centimeter.
  // The ping travels out and back, so to find the distance of the
  // object we take half of the distance travelled.
  return microseconds / 29 / 2;
}

void displayPING (void) {
  int sensorNr;
  
  // Display PING sensor readings (cm)
  for (sensorNr = 0; sensorNr < MAX_PING; sensorNr++) {
    Serial.print("Ping #");
    Serial.print(sensorNr + 1);
    Serial.print(" range = ");
    Serial.print(ping[sensorNr]);
    Serial.println(" cm");
  }
 
  Serial.println("");
}

/*
    Ping))) Sensor 
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

    Set units = true for inches, and false for cm
*/
int readPING (byte pingPin, boolean units) {
  long duration;
  int result;

  /*
    The PING))) is triggered by a HIGH pulse of 2 or more microseconds.
    Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  */
  pinMode(pingPin, OUTPUT);
  digitalWrite(pingPin, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(pingPin, LOW);

  /*
    The same pin is used to read the signal from the PING))): a HIGH
      pulse whose duration is the time (in microseconds) from the sending
      of the ping to the reception of its echo off of an object.

      pinMode(pingPin, INPUT);
      duration = pulseIn(pingPin, HIGH);
  */

  //  Convert the time into a distance
  if (units) {
    //  Return result in inches.
    result = microsecondsToInches(duration);
  } else {
    //  Return result in cm
    result = microsecondsToCentimeters(duration);
  }
 
  delay(100);
  
  return result;
}

/*
    Pulses a digital pin for a duration in ms
*/
void pulseDigital(int pin, int duration) {
  digitalWrite(pin, HIGH);   // Turn the ON by making the voltage HIGH (5V)
  delay(duration);           // Wait for duration ms
  digitalWrite(pin, LOW);    // Turn the pin OFF by making the voltage LOW (0V)
  delay(duration);           // Wait for duration ms
}

/*
    Display the data for a given sound sample
*/
int displaySoundSample (byte channel, Sample samples[MAX_SAMPLES]) {
  String st;
  int error = 0;

  if (! error) {  
    Serial.print(st);
    Serial.print(" Sample = ");
    Serial.print(samples[channel].value);
    Serial.print(", Voltage = ");
    Serial.print(samples[channel].volts);
    Serial.println(" volts");
  }

  return error;
}

/*
    Display the direction of a sound detection
*/
int displaySoundDirection (byte dir) {
  byte error = 0;

  if ((dir != 0) && (dir != NO_SOUND_DETECTED)) {
    Serial.print("Sound detected from the ");
    
    switch (dir) {
      case FRONT_LEFT_SIDE:
        Serial.print("Front Left");
        break;
      
      case FRONT_RIGHT_SIDE:
        Serial.print("Front Right");
        break;
      
      case BACK_LEFT_SIDE:
        Serial.print("Back Left");
        break;
      
      case BACK_RIGHT_SIDE:
        Serial.print("Back Right");
        break;
      
      default:
        Serial.print("Invalid");
        error = 100;
        break;
    }
    
    Serial.println(".");
  } else if (dir == NO_SOUND_DETECTED) {
    Serial.println("No sound detected.");
  }
  
  return error;
}

/*
    Get a sound sample from the given channel
*/
Sample soundSampleOf (byte channel) {
  Sample sample;
 
  sample.value = analogRead(channel);
  sample.volts = (sample.value * MAX_VOLTS) / MAX_STEPS;

  //  Initialize the rest of the sample
  sample.signalMin = 1024;
  sample.signalMax = 0;
  sample.signalMinVolts = 0.0;
  sample.signalMaxVolts = 0.0;
  sample.peakToPeakVolts = 0.0;

  return sample;
}

/*
    Get samples of sound from four microphones
*/
void getSoundSamples (Sample samples[MAX_SAMPLES]) {
  byte channel;
  Sample ts;

  //  Start of sample window
  unsigned long startMillis= millis();

  while ((millis() - startMillis) < sampleWindow) {
    /*
        Get and process raw samples from each microphone
    */
    for (channel = 0; channel < MAX_CHAN; channel++) {
      samples[channel] = soundSampleOf(channel);
      ts = samples[channel];

      if (ts.value < 1024) {
        //  Toss out spurious readings
        if (ts.value > ts.signalMax) {
          //  Save just the max levels
          ts.signalMax = ts.value;
          ts.signalMaxVolts = ts.volts;
        } else if (ts.value < ts.signalMin) {
          //  Save just the min levels
          ts.signalMin = ts.value;
          ts.signalMinVolts = ts.volts;
        }
        
        samples[channel] = ts;
      }
    }  
  } //  End of sample collection loop
  
  //  Calculate the peak to peak voltages
  for (channel = 0; channel < MAX_CHAN; channel++) {
    ts = samples[channel];
    ts.peakToPeakVolts = abs(ts.signalMaxVolts - ts.signalMinVolts); 

    samples[channel] = ts;
  }
}

/*
    Try to detect the loudest sound from one of four directions
*/
byte detectSound (void) {
  unsigned int sampleValue;
  Sample *ts;

  /*
      Variables for sound detection
  */
  double detectionFrontVolts = 0.0, detectionBackVolts = 0.0;
  byte detectionFront = 0;
  byte detectionBack = 0;
  byte detectionResult = 0;

  int displayPeakFrontLeft, displayPeakFrontRight;
  int displayPeakBackLeft, displayPeakBackRight; 

  /*
      Turn all the sound detection LEDs off
  */
  digitalWrite(FRONT_LEFT_LED, LOW);
  digitalWrite(FRONT_RIGHT_LED, LOW);
  digitalWrite(BACK_LEFT_LED, LOW);
  digitalWrite(BACK_RIGHT_LED, LOW);

  getSoundSamples(samples);

  /*
      Calculate the FRONT detection value
  */
  detectionFrontVolts = abs(samples[FRONT_LEFT_SIDE].peakToPeakVolts - samples[FRONT_RIGHT_SIDE].peakToPeakVolts);
//  Serial.print("Front Detection value = ");
//  Serial.println(detectionFrontVolts);

  /*
      Calculate the BACK detection value
  */
  detectionBackVolts = abs(samples[BACK_LEFT_SIDE].peakToPeakVolts - samples[BACK_RIGHT_SIDE].peakToPeakVolts);
//  Serial.print("Back Detection value = ");
//  Serial.println(detectionBackVolts);

  /*
      Get our final detection result
  */
  if ((detectionFrontVolts > detectionBackVolts) && (detectionFrontVolts > DETECTION_THRESHOLD)) {
    //  Check for sound detection
    if (samples[FRONT_LEFT_SIDE].peakToPeakVolts > samples[FRONT_RIGHT_SIDE].peakToPeakVolts) {
      digitalWrite(FRONT_LEFT_LED, HIGH);
      detectionFront = FRONT_LEFT_SIDE;
    } else if (samples[FRONT_RIGHT_SIDE].peakToPeakVolts > samples[FRONT_LEFT_SIDE].peakToPeakVolts) {
      digitalWrite(FRONT_RIGHT_LED, HIGH);
      detectionFront = FRONT_RIGHT_SIDE;
    } else {
      detectionFront = NO_SOUND_DETECTED;
    }
    
    detectionResult = detectionFront;
  } else if ((detectionBackVolts > detectionFrontVolts) && (detectionBackVolts > DETECTION_THRESHOLD)) {
    //  Check for sound detection
    if (samples[BACK_LEFT_SIDE].peakToPeakVolts > samples[BACK_RIGHT_SIDE].peakToPeakVolts) {
      digitalWrite(BACK_LEFT_LED, HIGH);
      detectionBack = BACK_LEFT_SIDE;
    } else if (samples[BACK_RIGHT_SIDE].peakToPeakVolts > samples[BACK_LEFT_SIDE].peakToPeakVolts) {
      digitalWrite(BACK_RIGHT_LED, HIGH);
      detectionBack = BACK_RIGHT_SIDE;
    } else {
      detectionBack = NO_SOUND_DETECTED;
    }

    detectionResult = detectionBack;
  }
  
  return detectionResult;
}

/*
    Move a servo by pulse width in ms (500ms - 2500ms)
*/
Servo moveServoPw (Servo servo, int servoPosition, int moveSpeed, int moveTime, boolean term) {
  Servo tServo = servo;
  
  tServo.error = 0;
  
  if ((servoPosition >= tServo.minPulse) && (servoPosition <= tServo.maxPulse)) {
    Serial.print("#");
    Serial.print(tServo.pin);
    Serial.print(" P");
    Serial.print(servoPosition + tServo.offset);

    tServo.msPulse = servoPosition;
    tServo.angle = ((servoPosition - SERVO_CENTER_MS) / 10);
    
    if (tServo.maxDegrees == 180) {
      tServo.angle += 90;
    }
  } else if ((servoPosition < tServo.minPulse) || (servoPosition > tServo.maxPulse)) {
    tServo.error = 200;
  }
 
  if (tServo.error == 0) {
    //  Add servo move speed
    if (moveSpeed != 0) {
      Serial.print(" S");
      Serial.print(moveSpeed);
    }
    
    //  Terminate the command
    if (term) {
      if (moveTime != 0) {
        Serial.print(" T");
        Serial.print(moveTime);
      }
      
      Serial.println();
    }
  }
  
  return tServo;
}

/*
    Move a servo by degrees (-90 to 90) or (0 - 180)
*/
Servo moveServoDegrees (Servo servo, int servoDegrees, int moveSpeed, int moveTime, boolean term) {
  Servo tServo = servo;
  int servoPulse = SERVO_CENTER_MS + servo.offset;

  tServo.error = 0;
  
  //  Convert degrees to ms for the servo move
  if (tServo.maxDegrees == 90) {
    servoPulse = (SERVO_CENTER_MS + tServo.offset) + (servoDegrees * 10);
  } else if (tServo.maxDegrees == 180) {
    servoPulse = (SERVO_CENTER_MS + tServo.offset) + ((servoDegrees - 90) * 10);
  }

  if ((servoPulse >= tServo.minPulse) && (servoPulse <= tServo.maxPulse)) {
    Serial.print("#");
    Serial.print(tServo.pin);
    Serial.print(" P");
    Serial.print(servoPulse);
    tServo.msPulse = (servoDegrees * 10) + SERVO_CENTER_MS;
    tServo.angle = servoDegrees;
    
    if (tServo.maxDegrees == 180) {
      tServo.angle += 90;
    }
  } else if ((servoPulse < tServo.minPulse) || (servoPulse > tServo.maxPulse)) {
    tServo.error = 200;
  }
  
  if (tServo.error == 0) {
    //  Add servo move speed
    if (moveSpeed != 0) {
      Serial.print(" S");
      Serial.print(moveSpeed);
    }
    
    //  Terminate the command
    if (term) {
      if (moveTime != 0) {
        Serial.print(" T");
        Serial.print(moveTime);
      }
      
      Serial.println();
    }
  }
  
  return tServo;
}

/*
    SetMotor (Packet Serial)
*/
void setMotor (int speed, boolean dir) {
}

/*
    Set motor speed and direction
*/
void setMotorPWM (byte motor, int spd, boolean dir) {
}

/*
    Called when a request from an I2C (Wire) Master comes in
*/
void wireRequestEvent (void) {
  Wire.write("Request");
}

//  Called when the I2C (Wire) Slave receives data from an I2C (Wire) Master
void wireReceiveData (int nrBytesRead) {
  byte command;
  int nrBytes = nrBytesRead - 1;
  
  Wire.write("Receive");
  
  if (Wire.available()) {
    command = Wire.read();
  }  
}

/*
    Process error conditions
*/
void processError (byte err) {
  Serial.print("Error: ");
  Serial.print(err);
  Serial.println("");
}

/*
    Setup routine - runs just one time
*/
void setup (void) {
  //  Start up the Wire library as a slave device at address 0xE0
  Wire.begin(NAV_I2C_ADDRESS);

  //  Register event handler
  Wire.onRequest(wireRequestEvent);
  Wire.onReceive(wireReceiveData);

  //  Initialize the hardware serial port  
  Serial.begin(115200);
  
  //  Initialize the LED pin as an output.
  pinMode(HEARTBEAT_LED, OUTPUT);
  
  //  Set the LED pins to be outputs  
  pinMode(COLOR_SENSOR_LED, OUTPUT);
  pinMode(FRONT_LEFT_LED, OUTPUT);
  pinMode(FRONT_RIGHT_LED, OUTPUT);
  pinMode(BACK_LEFT_LED, OUTPUT);
  pinMode(BACK_RIGHT_LED, OUTPUT);
 
  //  Test the LEDs
  digitalWrite(FRONT_LEFT_LED, HIGH);
  digitalWrite(FRONT_RIGHT_LED, HIGH);
  digitalWrite(BACK_LEFT_LED, HIGH);
  digitalWrite(BACK_RIGHT_LED, HIGH);

  delay(1000);

  digitalWrite(FRONT_LEFT_LED, LOW);
  digitalWrite(FRONT_RIGHT_LED, LOW);
  digitalWrite(BACK_LEFT_LED, LOW);
  digitalWrite(BACK_RIGHT_LED, LOW);
  digitalWrite(COLOR_SENSOR_LED, LOW);
  
  //  Put the front pan/tilt in home position
  panServo = moveServoPw(panServo, SERVO_CENTER_MS, 0, 0, false);
  tiltServo = moveServoPw(tiltServo, SERVO_CENTER_MS, 0, 0, true);
//  panServo = moveServoDegrees(panServo, moveDegrees, moveSpeed, moveTime, false);
//  panServo = moveServoDegrees(tiltServo, moveDegrees, moveSpeed, moveTime, false);
}

/*
    The loop routine runs forever
*/
void loop (void) {
  byte error = 0;
  byte directionOfSound = 0;

  int analogPin = 0;
  int digitalPin = 0;
  
  // Pulse the heartbeat LED
  pulseDigital(HEARTBEAT_LED, 500);

  if (MAX_GP2D12 > 0) {
    //  Get distance readings from the GP2D12 Analog IR sensors and store the readings  
    for (analogPin = 0; analogPin < MAX_GP2D12; analogPin++) { 
      gp2d12[analogPin] = readGP2D12b(analogPin);
    }
  
    displayGP2D12();
  }

  if (MAX_PING > 0) {
    //  Get distance readings from PING Ultrasonic sensors in cm and store the readings
    for (digitalPin = 0; digitalPin < MAX_PING; digitalPin++) {
      ping[digitalPin] = readPING(digitalPin + DIGITAL_PIN_BASE, false);
    }
  }

  //  Do sound detection
  directionOfSound = detectSound();
//  error = displaySoundDirection(directionOfSound);

  if (error != 0) {
    processError(error);
  }
}
