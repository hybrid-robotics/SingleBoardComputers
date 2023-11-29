/*
  Blink4
  Turns each of 4 LEDs on in sequence, for a time, then off, repeatedly.
*/

#define  TIME  250

void setup() {                
  //  Initialize the digital pins as outputs.
  for (int8_t ledPin = 2; ledPin < 6; ledPin++) {
    pinMode(ledPin, OUTPUT);
  }    
}

void loop() {
  //  For each LED..
  for (int8_t ledPin = 2; ledPin < 6; ledPin++) {
    //  Blink a few times
    for (int8_t b = 0; b < 10; b++) {
      digitalWrite(ledPin, HIGH);      //  Set the LED on
      delay(TIME);                     //  Wait for a bit
      digitalWrite(ledPin, LOW);       //  Set the LED off
      delay(TIME);                     //  Wait for a bit  
    }
  }  
}
