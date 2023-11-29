#include <Servo.h>

Servo mainPan, mainTilt;

void setup() {
  // put your setup code here, to run once:
  mainPan.attach(2);
  mainPan.writeMicroseconds(1500);
  
  mainTilt.attach(3);
  mainTilt.writeMicroseconds(1500);
}

void loop() {
  // put your main code here, to run repeatedly:

}
