#Set up I2C
bus=smbus.SMBus(0)
bus.write_byte(0x35,0x80)
bus.write_byte(0x35,0x01)
buffer=bus.read_i2c_block_data(0x40,0xe3,2)
#buffer=[1,2]
print ("%02x %02x" % (buffer[0], buffer[1]))
advalue = 256*int(buffer[1]) + int(buffer[0])
print ("advalue = %d" % advalue)