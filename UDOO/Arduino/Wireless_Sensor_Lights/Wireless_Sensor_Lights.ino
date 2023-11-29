/*
	Program:		Wireless_Sensor_Lights.ino - A wireless experiment at 433 MHz
	Date:			17-Feb-2014
	Version:		0.0.1 Arduino Decimilia - ALPHA

	Purpose:		To experiment with low cost, low-speed, low-bandwidth, long range wireless sensor
						nodes, because sensors typically don't need to send a lot of data.
						
	Dependencies:	Adafruit libraries:
						Adafruit_DHT_Sensor, Adafruit_LEDBackpack, and Adafruit_GFX libraries (for the displays)

	Comments:		Credit is given, where applicable, for code I did not originate.

					Copyright (C) 2013 Dale Weber <hybotics.pdx@gmail.com>.
*/
#include <SoftwareSerial.h>
#include <Adafruit_LEDBackpack.h>
#include <Adafruit_GFX.h>
#include <Adafruit_DHT_Sensor.h>
#include <Adafruit_NeoPixel.h>

#include "Wireless_Sensor_Lights.h"

/*
	Initialize Objects
*/

Adafruit_DHT_Sensor dht22 = Adafruit_DHT_Sensor(DHT_SENSOR_PIN, DHT_SENSOR_TYPE);

Adafruit_8x8matrix matrix8x8 = Adafruit_8x8matrix();

//	Hardware Serial: Console and debug (replaces Serial.* routines)
SoftwareSerial console(SERIAL_CONSOLE_RX_PIN, SERIAL_CONSOLE_TX_PIN);

/*
	Initialize Global Variables
*/

/*
	Code starts here.
*/

/*
	Convert a temperature in Celsius to Fahrenheit
*/
float toFahrenheit (float celsius) {
	return (celsius * 1.8) + 32;
}

void displayReadings (float humidity, float fahrenheit, float celsius) {
    console.print("Humidity: "); 
    console.print(humidity);
    console.print("Temperature: "); 
    console.print(fahrenheit);
    console.print(" F, ");
    console.print(celsius);
    console.println(" C.");
}

/*
    Pulses a digital pin for a duration in ms
*/
void pulseDigital(int pin, int duration) {
	digitalWrite(pin, HIGH);			// Turn the ON by making the voltage HIGH (5V)
	delay(duration);					// Wait for duration ms
	digitalWrite(pin, LOW);				// Turn the pin OFF by making the voltage LOW (0V)
	delay(duration);					// Wait for duration ms
}

/*
	Receive a nybble (4 bits) of data
*/
void receiveNybble (void) {
	byte bit = 0;
}

/*
	Send a nybble (4 bits) of data
*/
void sendNybble (byte data) {
	byte bit = 0;

	//	Set the transmit bits - we only look at the lower four bits
	for (bit = 0; bit < 4; bit++) {
		digitalWrite(TRANSMITTER_PIN_BASE + bit, (data & (bit ^ 2)));
	}

	//	There MUST be a signal that triggers the transmitter to transmit..
}

/*
	Break a float data variable into four bit nybbles and transmit it
*/
bool transmitFloat (float value) {
	bool status = true;

	return status;
}

void setup (void) {
	//  Initialize the console port
	console.begin(115200);

	console.println();
	console.print("Wireless Sensors and Lights, version ");
	console.print(BUILD_VERSION);
	console.print(" on ");
	console.print(BUILD_DATE);
	console.print(" for the ");
	console.print(BUILD_BOARD);
	console.println(" board");

	//	Initialize the display
	matrix8x8.begin(MATRIX_DISPLAY_ADDRESS);

	//	Initialize the DHT22 Temperature and Humidity sensor
	dht22.begin();
}

void loop (void) {
	bool status;
	byte input = 0, output = 0;
	float humidity, celsius, fahrenheit;

	//	Tell everyone we are here
	pulseDigital(HEARTBEAT_LED, 250);

	//	Reading temperature or humidity takes about 250 milliseconds!
	//	Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
	humidity = dht22.readHumidity();
	celsius = dht22.readTemperature();
	fahrenheit = toFahrenheit(celsius);

	//	Check if returns are valid. If they are NaN (not a number) then something went wrong!
	if (isnan(celsius) || isnan(humidity)) {
		console.println("Error: Failed to read the DHT22 sensor!");
	} else {
		displayReadings(humidity, fahrenheit, celsius);
	}

	/*
		Send the readings out
	*/
	status = transmitFloat(humidity);

	if (!status) {
		console.println("Error: Unable to transmit the humidity reading!");
	}

	status = transmitFloat(fahrenheit);

	if (!status) {
		console.println("Error: Unable to transmit the fahrenheit temperature reading!");
	}

	status = transmitFloat(celsius);

	if (!status) {
		console.println("Error: Unable to transmit the celsius temperature reading!");
	}

	//	Make sure we give the sensor enough time in between attempts to read it
	delay(5000);
}
