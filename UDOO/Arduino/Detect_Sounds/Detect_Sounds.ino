/****************************************
Scrolling Sound Meter Sketch for the 
Adafruit Microphone Amplifier
****************************************/
#include <Wire.h>
#include "Adafruit_LEDBackpack.h"
#include "Adafruit_GFX.h"

//  Detection threshold
#define  THRESHOLD   0.20

#define  COLOR_LED   2
#define  LEFT_LED    3
#define  RIGHT_LED   4

#define  LEFT_MIC    0
#define  RIGHT_MIC   1

#define  MAX_VOLTS   5.0
#define  MAX_STEPS   1024.0

const int maxScale = 8;
const int redZone = 5;

//  Sample window width in mS (50 mS = 20Hz)
const int sampleWindow = 50;

void setup() {
  Serial.begin(115200);
  
  //  Set the LED pins to be outputs  
  pinMode(COLOR_LED, OUTPUT);
  pinMode(LEFT_LED, OUTPUT);
  pinMode(RIGHT_LED, OUTPUT);
  
  //  Test the LEDs
  digitalWrite(LEFT_LED, HIGH);
  digitalWrite(RIGHT_LED, HIGH);
  delay(1000);
  digitalWrite(LEFT_LED, LOW);
  digitalWrite(RIGHT_LED, LOW);
  digitalWrite(COLOR_LED, LOW);
}

void loop() {
    unsigned long startMillis= millis();  // Start of sample window

    unsigned int sampleLeft, sampleRight;
    unsigned int signalMinLeft = 1024, signalMaxLeft = 0;
    unsigned int signalMinRight = 1024, signalMaxRight = 0;
    
    double sampleLeftVolts, sampleRightVolts;
    double signalMinLeftVolts, signalMaxLeftVolts;
    double signalMinRightVolts,signalMaxRightVolts;
    double detection, peakToPeakLeftVolts, peakToPeakRightVolts;

    int displayPeakLeft, displayPeakRight; 
   
    while (millis() - startMillis < sampleWindow) {
      sampleLeft = analogRead(LEFT_MIC);
      sampleLeftVolts = (sampleLeft * MAX_VOLTS) / MAX_STEPS;
      
      sampleRight = analogRead(RIGHT_MIC);
      sampleRightVolts = (sampleRight * MAX_VOLTS) / MAX_STEPS;
/*
      Serial.print("Sample left = ");
      Serial.print(sampleLeft);
      Serial.print(", Voltage = ");
      Serial.print(sampleLeftVolts);
      Serial.println(" volts");

      Serial.print("Sample right = ");
      Serial.print(sampleRight);
      Serial.print(", Voltage = ");
      Serial.print(sampleRightVolts);
      Serial.println(" volts");
*/      
      if (sampleLeft < 1024) {
        //  Toss out spurious readings
        if (sampleLeft > signalMaxLeft) {
          //  Save just the max levels
          signalMaxLeft = sampleLeft;
          signalMaxLeftVolts = sampleLeftVolts;
        } else if (sampleLeft < signalMinLeft) {
          //  Save just the min levels
          signalMinLeft = sampleLeft;
          signalMinLeftVolts = sampleLeftVolts;
        }
      }
      
      if (sampleRight < 1024) {
        //  Toss out spurious readings
        if (sampleRight > signalMaxRight) {
          //  Save just the max levels
          signalMaxRight = sampleRight;
          signalMaxRightVolts = sampleRightVolts;
        } else if (sampleRight < signalMinRight) {
          //  Save just the min levels
          signalMinRight = sampleRight;
          signalMinRightVolts = sampleRightVolts;
        }
      }
    }

    /*
        Process LEFT channel
    */   
    peakToPeakLeftVolts = signalMaxLeftVolts - signalMinLeftVolts;
/*   
    Serial.print("Left peak to peak = ");
    Serial.print(peakToPeakLeftVolts);
    Serial.println(" volts");
    
    Serial.print("Left: Min = ");
    Serial.print(signalMinLeftVolts);
    Serial.print(", Max = ");
    Serial.print(signalMaxLeftVolts);
    Serial.println(" (volts)");
*/   
    /*
        Process RIGHT channel
    */   
    peakToPeakRightVolts = signalMaxRightVolts - signalMinRightVolts;
/*
    Serial.print("Right peak to peak = ");
    Serial.print(peakToPeakRightVolts);
    Serial.println(" volts");
    
    Serial.print("Right: Min = ");
    Serial.print(signalMinRightVolts);
    Serial.print(", Max = ");
    Serial.print(signalMaxRightVolts);
    Serial.println(" (volts)");
*/
    //  Set a threshold for making a detection
    detection = abs(peakToPeakLeftVolts - peakToPeakRightVolts);
    Serial.print("Detection value = ");
    Serial.println(detection);

    if (detection > THRESHOLD) {
      //  Check for sound detection
      if (peakToPeakLeftVolts > peakToPeakRightVolts) {
        digitalWrite(LEFT_LED, HIGH);
        digitalWrite(RIGHT_LED, LOW);
        Serial.println("LEFT side");
      } else if (peakToPeakRightVolts > peakToPeakLeftVolts) {
        digitalWrite(LEFT_LED, LOW);
        digitalWrite(RIGHT_LED, HIGH);
        Serial.println("RIGHT side");
      }
    } else {
        digitalWrite(LEFT_LED, LOW);
        digitalWrite(RIGHT_LED, LOW);
    }
}
