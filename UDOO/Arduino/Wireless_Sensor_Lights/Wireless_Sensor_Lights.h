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

#ifndef		__WIRELESS_SENSOR_LIGHTS_H__
#define		__WIRELESS_SENSOR_LIGHTS_H__

//	The standard board LED
#define		HEARTBEAT_LED      	        13

//	Software version information
#define		BUILD_VERSION				"0.0.1"
#define		BUILD_DATE 					"17-Feb-2014"
#define		BUILD_BOARD					"Arduino Decimila"

//	Display constants
#define		MATRIX_DISPLAY_ADDRESS		0x73

/*
	Hardware Serial ports
*/
//	Serial:	Console and Debug port
#define	SERIAL_CONSOLE_RX_PIN			0
#define	SERIAL_CONSOLE_TX_PIN			1

//	NeoPixel constants
#define		NEOPIXEL_PIN_STRIP			NEOPIXEL_PIN_STRIP8
#define		NEOPIXEL_MAX_STRIP			NEOPIXEL_MAX_STRIP8

#define		NEOPIXEL_PIN_STRIP8			2
#define		NEOPIXEL_MAX_STRIP8			8

#define		NEOPIXEL_PIN_STRIP12		2
#define		NEOPIXEL_MAX_STRIP12		12

#define		NEOPIXEL_PIN_RING12			2
#define		NEOPIXEL_MAX_RING12			12

#define		NEOPIXEL_PIN_RING16			2
#define		NEOPIXEL_MAX_RING16			16

#define		NEOPIXEL_PIN_RING24			2
#define		NEOPIXEL_MAX_RING24			24

/*	DHT sensor definitions

	Uncomment the type you're using.
*/
//#define		DHT_SENSOR_TYPE				DHT11		//	DHT 11 
//#define		DHT_SENSOR_TYPE				DHT21		//	DHT 21 (AM2301)
#define		DHT_SENSOR_TYPE				DHT22 		//	DHT 22 (AM2302)
#define		DHT_SENSOR_PIN				3

//	433 MHz Transmitter and Receiver definitions
#define		RECEIVER_PIN_BASE			RECEIVER_D0_PIN

#define		RECEIVER_D0_PIN				4
#define		RECEIVER_D1_PIN				5
#define		RECEIVER_D2_PIN				6
#define		RECEIVER_D3_PIN				7

#define		TRANSMITTER_PIN_BASE		TRANSMITTER_D0_PIN

#define		TRANSMITTER_D0_PIN			8
#define		TRANSMITTER_D1_PIN			9
#define		TRANSMITTER_D2_PIN			10
#define		TRANSMITTER_D3_PIN			11

struct NeoPixel {
	uint16_t pixel;
	Adafruit_NeoPixel *strip;
	boolean currState;
	uint32_t currColor;

	boolean isBlinking;
	uint16_t waitMS;
};

struct NeoPixelStrip {
	Adafruit_NeoPixel *strip;
	NeoPixel pixels[];
};

#endif
