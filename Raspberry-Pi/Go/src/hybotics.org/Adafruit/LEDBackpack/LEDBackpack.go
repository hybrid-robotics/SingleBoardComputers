/*
	LEDBackpack - based on the Adafruit Python library by the same name.
*/
package ledbackpack

import (
	"errors"
	"log"
	"fmt"
	"github.com/hybotics/i2c"
)

const (
	//	Registers
	__HT16K33_REGISTER_DISPLAY_SETUP        = 0x80
	__HT16K33_REGISTER_SYSTEM_SETUP         = 0x20
	__HT16K33_REGISTER_DIMMING              = 0xE0
        
	//	Blink rate
	__HT16K33_BLINKRATE_OFF                 = 0x00
	__HT16K33_BLINKRATE_2HZ                 = 0x01
	__HT16K33_BLINKRATE_1HZ                 = 0x02
	__HT16K33_BLINKRATE_HALFHZ              = 0x03
)
                  
type LEDBackpack struct {
	address byte
	bus *i2c.I2CBus
    
	//  Display buffer (8x16-bits)
	__buffer [8]uint16

	dataWrite bool
	lastData byte
	lastRegister byte
}

func (l *LEDBackpack) Init (addr, busNr byte) (err error) {
	l.address = addr

	l.lastData = 0
	l.dataWrite = false

	//	The Raspberry Pi Model B uses I2C Bus #1
	l.bus, err = i2c.Bus(busNr)

	return
}

func (l *LEDBackpack) WriteByte (reg, data byte) (err error) {
	err = l.bus.WriteByte(l.address, reg, data)
	
	if err != nil {
		etxt := fmt.Sprintf("LEDBackpack.WriteByte/%s", err)
		err = errors.New(etxt)
	} else {
		l.lastData = data
		l.lastRegister = reg
		l.dataWrite = true
	}
	
	return
}

func main () {
	var LED8x8 LEDBackpack

	fmt.Println("Raspberry Pi I2C Test in Go")

	err := LED8x8.Init(0x70, 1)

	if err != nil {
		log.Fatal(err)
	}
	
	err = LED8x8.WriteByte(0x0, 0x0)

	if err != nil {
		log.Fatal(err)
	}	
}
