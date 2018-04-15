from smbus import SMBus
#Primitives for manally setting up the ADC
def i2cInit(i2cID):
    return SMBus(i2cID)
def adInit(bus):
    bus.write_byte(0x35, 0x80)
    bus.write_byte(0x35, 0x01)    
def readAD(bus):
    buffer = bus.read_i2c_block_data(0x40, 0xe3, 2)
    return 256 * int(buffer[1]) + int(buffer[0])
#Object oriented form as well, because WHY NOT?
class ADC:
    def __init__(self, i2cBusID):
        self.i2cBus = i2cInit(i2cBusID)
    def setup(self):
        adInit(self.i2cBus)
    def getValue(self):
        return readAD(self.i2cBus)
    def getI2CBus(self):
        return self.i2cBus

#### Original code for reference
##Set up I2C
#bus=SMBus(0)
#bus.write_byte(0x35,0x80)
#bus.write_byte(0x35,0x01)
#buffer=bus.read_i2c_block_data(0x40,0xe3,2)
##buffer=[1,2]
#print ("%02x %02x" % (buffer[0], buffer[1]))
#advalue = 256*int(buffer[1]) + int(buffer[0])
#print ("advalue = %d" % advalue)