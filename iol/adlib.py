from cli import colors

class ADC:
	def __init__(self, i2cID):
		from smbus import SMBus
		self.i2cBus = SMBus(i2cID)
		self.i2cID = i2cID
	def setup(self):
		bus.write_byte(0x35, 0x80)
		bus.write_byte(0x35, 0x01)  
	def getValue(self):
		buffer = bus.read_i2c_block_data(0x40, 0xe3, 2)
		return 256 * int(buffer[1]) + int(buffer[0])
      
class EmulatedADC:
	def __init__(self, i2cID):
		print(colors.cyan + "Initialized ADC on I2C bus ID: " + str(i2cID) + colors.reset)
		self.i2cID = i2cID
	def setup(self):
		print(colors.cyan + "Setup ADC on I2C bus ID: " + str(self.i2cID) + colors.reset)
	def getValue(self):
		return 0