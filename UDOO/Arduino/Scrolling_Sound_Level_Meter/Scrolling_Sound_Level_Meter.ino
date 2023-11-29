/****************************************
Scrolling Sound Meter Sketch for the 
Adafruit Microphone Amplifier
****************************************/

#include <Wire.h>
#include "Adafruit_LEDBackpack.h"
#include "Adafruit_GFX.h"

#define  LEFT_MIC    0
#define  RIGHT_MIC   1

#define  MAX_VOLTS   5.0
#define  MAX_STEPS   1024.0

// Include the Matrix code for display
//Adafruit_8x8matrix matrix = Adafruit_8x8matrix();

const int maxScale = 8;
const int redZone = 5;

//  Sample window width in mS (50 mS = 20Hz)
const int sampleWindow = 50;


void setup() {
  Serial.begin(115200);
  
  //  Pass in the address
//  matrix.begin(0x71);
}


void loop() {
    unsigned long startMillis= millis();  // Start of sample window
    unsigned int peakToPeakLeft, peakToPeakRight = 0;   // peak-to-peak levels

    unsigned int signalMaxLeft = 0, signalMaxRight = 0;
    unsigned int signalMinLeft = 1024, signalMinRight = 1024;

    double realVoltsLeft, peakVoltsLeft, realVoltsRight, peakVoltsRight;
    int displayPeakLeft, displayPeakRight;
    unsigned int sampleLeft, sampleRight;
   
    while (millis() - startMillis < sampleWindow) {
      sampleLeft = analogRead(LEFT_MIC);
      sampleRight = analogRead(RIGHT_MIC);
      
      if (sampleLeft < 1024) {
        //  Toss out spurious readings
        if (sampleLeft > signalMaxLeft) {
          //  Save just the max levels
          signalMaxLeft = sampleLeft;
        } else if (sampleLeft < signalMinLeft) {
          //  Save just the min levels
          signalMinLeft = sampleLeft;
        }
      }
      
      if (sampleRight < 1024) {
        //  Toss out spurious readings
        if (sampleRight > signalMaxRight) {
          //  Save just the max levels
          signalMaxRight = sampleRight;
        } else if (sampleRight < signalMinRight) {
          //  Save just the min levels
          signalMinRight = sampleRight;
        }
      }
    }

    //  Left channel   
    peakToPeakLeft = signalMaxLeft - signalMinLeft;
/*
    Serial.print("Left sample = ");
    Serial.println(sampleLeft);
    
    Serial.print("Left peak to peak = ");
    Serial.println(peakToPeakLeft);
*/    
    realVoltsLeft = (sampleLeft * MAX_VOLTS) / MAX_STEPS;
/*
    Serial.print("Real left = ");
    Serial.print(realVoltsLeft);
    Serial.println(" volts");
*/    
    //  Convert to volts
    peakVoltsLeft = (peakToPeakLeft * MAX_VOLTS) / MAX_STEPS;
    Serial.print("Peak to peak left = ");
    Serial.print(peakVoltsLeft);
    Serial.println(" volts");
   
    //  Map 1v p-p level to the max scale of the display
    displayPeakLeft = map(peakToPeakLeft, 0, 1023, 0, maxScale);

    //  Right channel   
    peakToPeakRight = signalMaxRight - signalMinRight;
/*
    Serial.print("Right sample = ");
    Serial.println(sampleRight);
    
    Serial.print("Right peak to peak = ");
    Serial.println(peakToPeakRight);
*/    
    realVoltsRight = (sampleRight * MAX_VOLTS) / MAX_STEPS;
/*
    Serial.print("Real right = ");
    Serial.print(realVoltsRight);
    Serial.println(" volts");
*/
    //  Convert to volts
    peakVoltsRight = (peakToPeakRight * MAX_VOLTS) / MAX_STEPS;
    Serial.print("Peak to peak right = ");
    Serial.print(peakVoltsRight);
    Serial.println(" volts");
   
    //  Map 1v p-p level to the max scale of the display
    displayPeakRight = map(peakToPeakRight, 0, 1023, 0, maxScale);
    
    Serial.println();

/*
   //  Update the display:
   for (int i = 0; i < 7; i++) {  // shift the display left
      matrix.displaybuffer[i] = matrix.displaybuffer[i+1];
   }
   

   //  Draw the new sample
   for (int i = 0; i <= maxScale; i++) {
      if (i >= displayPeak) { // blank these pixels
         matrix.drawPixel(i, 7, 0);
      } else if (i < redZone) { // draw in green
         matrix.drawPixel(i, 7, LED_GREEN);
      } else { // Red Alert!  Red Alert!
         matrix.drawPixel(i, 7, LED_RED);
      }
   }

   //  Write the changes we just made to the display
   matrix.writeDisplay();
*/
  delay(3000);
}
