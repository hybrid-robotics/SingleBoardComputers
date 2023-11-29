'''
	This is a library for the L3GD20 GYROSCOPE from Adafruit (http://www.adafruit.com)

	Designed specifically to work with the Adafruit L3GD20 Breakout 
		----> https://www.adafruit.com/products/1032

	These sensors use I2C or SPI to communicate, 2 pins (I2C) 
		or 4 pins (SPI) are required to interface.

	Adafruit invests time and resources providing this open source code,
		please support Adafruit and open-source hardware by purchasing
		products from Adafruit!

	Written by Kevin "KTOWN" Townsend for Adafruit Industries.

	BSD license, all text above must be included in any redistribution
	
	Ported to Python by Dale Weber, hybotics.pdx@gmail.com and @hybotics on App.Net
		This is as direct a port of the Adafruit Arduino library by the same name as possible.

		06-Jan-2014		0.1.0	Started port

'''

from Adafruit_I2C import Adafruit_I2C

class Hybotics_L3GD20 (Adafruit_I2C):
	i2c = None
	address = None
	debug = None

	#	Data values
	_data_x = 0.0
	_data_y = 0.0
	_data_z = 0.0

	_cs = None
	_miso = None
	_mosi = None
	_clk = None
        
	L3GD20_ADDRESS							= (0x6B)			# 1101011
	L3GD20_POLL_TIMEOUT						= (100)				# Maximum number of read attempts
	L3GD20_ID								= (0B11010100)

	L3GD20_SENSITIVITY_250DPS				= (0.00875F)		# Roughly 22/256 for fixed point match
	L3GD20_SENSITIVITY_500DPS				= (0.0175F)			# Roughly 45/256
	L3GD20_SENSITIVITY_2000DPS				= (0.070F)			# Roughly 18/256
	L3GD20_DPS_TO_RADS						= (0.017453293F)	# Degress/s to rad/s multiplier

	l3gd20Registers_t = {										# DEFAULT    TYPE
		"L3GD20_REGISTER_WHO_AM_I":			0x0F,				# 11010100   r
		"L3GD20_REGISTER_CTRL_REG1":		0x20,				# 00000111   rw
		"L3GD20_REGISTER_CTRL_REG2":		0x21,				# 00000000   rw
      	"L3GD20_REGISTER_CTRL_REG3":		0x22,				# 00000000   rw
		"L3GD20_REGISTER_CTRL_REG4":		0x23,				# 00000000   rw
		"L3GD20_REGISTER_CTRL_REG5":		0x24,				# 00000000   rw
		"L3GD20_REGISTER_REFERENCE":		0x25,				# 00000000   rw
		"L3GD20_REGISTER_OUT_TEMP":			0x26,				#            r
		"L3GD20_REGISTER_STATUS_REG":		0x27,				#            r
		"L3GD20_REGISTER_OUT_X_L":			0x28,				#            r
		"L3GD20_REGISTER_OUT_X_H":			0x29,				#            r
		"L3GD20_REGISTER_OUT_Y_L":			0x2A,				#            r
		"L3GD20_REGISTER_OUT_Y_H":			0x2B,				#            r
		"L3GD20_REGISTER_OUT_Z_L":			0x2C,				#            r
		"L3GD20_REGISTER_OUT_Z_H":			0x2D,				#            r
		"L3GD20_REGISTER_FIFO_CTRL_REG":	0x2E,				# 00000000   rw
		"L3GD20_REGISTER_FIFO_SRC_REG":		0x2F,				#            r
		"L3GD20_REGISTER_INT1_CFG":			0x30,				# 00000000   rw
		"L3GD20_REGISTER_INT1_SRC":			0x31,				#            r
		"L3GD20_REGISTER_TSH_XH":			0x32,				# 00000000   rw
		"L3GD20_REGISTER_TSH_XL":			0x33,				# 00000000   rw
		"L3GD20_REGISTER_TSH_YH":			0x34,				# 00000000   rw
		"L3GD20_REGISTER_TSH_YL":			0x35,				# 00000000   rw
		"L3GD20_REGISTER_TSH_ZH":			0x36,				# 00000000   rw
		"L3GD20_REGISTER_TSH_ZL":			0x37,				# 00000000   rw
		"L3GD20_REGISTER_INT1_DURATION":	0x38				# 00000000   rw
    }
    
    l3gd20Range_t = {
		"L3DS20_RANGE_250DPS":				1,
		"L3DS20_RANGE_500DPS":				2,
		"L3DS20_RANGE_2000DPS":				3
    };

    l3gd20Data_s {
      "x": _data_x,												# float
      "y": _data_y,												# float
      "z": _data_z												# float
    }
	__L3GD20_ADDRESS						= (0x6B)			#	1101011
	__L3GD20_POLL_TIMEOUT					= (100)				#	Maximum number of read attempts
	__L3GD20_ID								= (0b11010100)

	__L3GD20_SENSITIVITY_250DPS				= (0.00875F)		#	Roughly 22/256 for fixed point match
	__L3GD20_SENSITIVITY_500DPS				= (0.0175F)			#	Roughly 45/256
	__L3GD20_SENSITIVITY_2000DPS			= (0.070F)			#	Roughly 18/256
	__L3GD20_DPS_TO_RADS					= (0.017453293F)	#	Degress/s to rad/s multiplier

	#	L3GD20 Registers											DEFAULT    TYPE
	__L3GD20_REGISTER_WHO_AM_I				= 0x0F				#	11010100	r
	__L3GD20_REGISTER_CTRL_REG1				= 0x20				#	00000111	rw
	__L3GD20_REGISTER_CTRL_REG2				= 0x21				#	00000000	rw
	__L3GD20_REGISTER_CTRL_REG3				= 0x22				#	00000000	rw
	__L3GD20_REGISTER_CTRL_REG4				= 0x23				#	00000000	rw
	__L3GD20_REGISTER_CTRL_REG5				= 0x24				#	00000000	rw
	__L3GD20_REGISTER_REFERENCE				= 0x25				#	00000000	rw
	__L3GD20_REGISTER_OUT_TEMP				= 0x26				#				r
	__L3GD20_REGISTER_STATUS_REG			= 0x27				#				r
	__L3GD20_REGISTER_OUT_X_L				= 0x28				#				r
	__L3GD20_REGISTER_OUT_X_H				= 0x29				#				r
	__L3GD20_REGISTER_OUT_Y_L				= 0x2A				#				r
	__L3GD20_REGISTER_OUT_Y_H				= 0x2B				#				r
	__L3GD20_REGISTER_OUT_Z_L				= 0x2C				#				r
	__L3GD20_REGISTER_OUT_Z_H				= 0x2D				#				r
	__L3GD20_REGISTER_FIFO_CTRL_REG			= 0x2E				#	00000000	rw
	__L3GD20_REGISTER_FIFO_SRC_REG			= 0x2F				#				r
	__L3GD20_REGISTER_INT1_CFG				= 0x30				#	00000000	rw
	__L3GD20_REGISTER_INT1_SRC				= 0x31				#				r
	__L3GD20_REGISTER_TSH_XH				= 0x32				#	00000000	rw
	__L3GD20_REGISTER_TSH_XL				= 0x33				#	00000000	rw
	__L3GD20_REGISTER_TSH_YH				= 0x34				#	00000000	rw
	__L3GD20_REGISTER_TSH_YL				= 0x35				#	00000000	rw
	__L3GD20_REGISTER_TSH_ZH				= 0x36				#	00000000	rw
	__L3GD20_REGISTER_TSH_ZL				= 0x37				#	00000000	rw
	__L3GD20_REGISTER_INT1_DURATION			= 0x38				#	00000000	rw

	#	Ranging modes
	__L3DS20_RANGE_250DPS					= 1
	__L3DS20_RANGE_500DPS					= 2
	__L3DS20_RANGE_2000DPS					= 3

    l3gd20Range_t range;

	l3gd20Data data;											#	Last read will be available here

	'''                                                              
    struct l3gd20Data_s {
      float x;
      float y;
      float z;
    };
    '''
    
	#	Constructor
	def __init__ (self, address=self.__L3GD20_ADDRESS, debug=False, cs=-1, miso=-1, mosi=-1, clk=-1):
		self.i2c = Adafruit_I2C(address)

		self.address = address
		self.debug = debug

		self._cs = cs;
		self._miso = miso;
		self._mosi = mosi;
		self._clk = clk;
        
		return None

	def bool begin (self, rng=self.__L3DS20_RANGE_250DPS, addr=self.__L3GD20_ADDRESS):

		return None

    def read (self):

		return None

	def write8 (self, l3gd20Registers_t reg, byte value);

		return None

    def byte read8 (self, l3gd20Registers_t reg):
    
    	return None
