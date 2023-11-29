#include <MozziGuts.h>
#include <Oscil.h>
#include <tables/sin2048_int8.h>

#include "MozziTest.h"

Oscil <2048, AUDIO_RATE> aSin(SIN2048_DATA);

void updateControl (void) {

}

int updateAudio (void) {

}

void setup() {
	//	Put your setup code here, to run once:
	startMozzi(CONTROL_RATE);
	aSin.setFreq(440);
}

void loop() {
	//	Put your main code here, to run repeatedly:
	audioHook();
}
