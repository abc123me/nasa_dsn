import time
import smbus
import pygpio

#Set up I2C
bus=smbus.SMBus(0)
bus.write_byte(0x35,0x80)
bus.write_byte(0x35,0x01)
buffer=bus.read_i2c_block_data(0x40,0xe3,2)
#buffer=[1,2]
print ("%02x %02x" % (buffer[0], buffer[1]))
advalue = 256*int(buffer[1]) + int(buffer[0])
print ("advalue = %d" % advalue)

pin7 = pygpio.GPIOPin(4)
pin7.setMode(False)

pin8 = pygpio.GPIOPin(14)
pin8.setMode(False)

pin10 = pygpio.GPIOPin(15)
pin10.setMode(False)

pin11 = pygpio.GPIOPin(17)
pin11.setMode(False)

pin12 = pygpio.GPIOPin(18)
pin12.setMode(False)

pin13 = pygpio.GPIOPin(27)
pin13.setMode(False)

pin26 = pygpio.GPIOPin(7)
pin26.setMode(True)

pin27= pygpio.GPIOPin(IDSD)
pin27.setMode(True)

pin23 = pygpio.GPIOPin(11)
pin23.setMode(True)

pin24 = pygpio.GPIOPin(8)
pin24.setMode(True)

pin21 = pygpio.GPIOPin(9)
pin21.setMode(True)

pin22 = pygpio.GPIOPin(25)
pin22.setMode(True)

print(str(rdbbsw(1)) + ", " + str(rdbbsw(2)))

def rdbbsw(1)
    #Read baseball switch 1 status
    read(4)
    return valueOfPin
    #pin 7, 8 (GPIO 4, 14)
def rdbbsw(2)
    #Read baseball switch 2 status
    #pin 10, 11 (GPIO 15, 17)
    return valueOfPin
def rdbbsw(3)
    #Read baseball switch 3 status
    #pin 12, 13 (GPIO 18, 27)
    return valueOfPin
def wrbbsw(1)
    #Turn on/off baseball switch 1
    #pin 26(pos 0), 27(pos 1) (GPIO 7, IDSD)
    if bbsval1 = 0
        write(7,1)       
        write(ID_SD,0)
    if bbsval1 = 1
        write(ID_SD,1)
        write(7,0)
def wrbbsw(2)
    #Turn on/off baseball switch 2
    #pin 23(pos 0), 24(pos 1) (GPIO 11, 8)
    if bbsval1 = 0
        write(11,1)
        write(8,0)
    if bbsval1 = 1
        write(8,1)
        write(11,0)
def wrbbsw(3)
    #Turn on/off baseball switch 3
    #pin 21(pos 0), 22(pos 1) (GPIO 9, 25)
    if bbsval1 = 0
        write(9,1)
        write(25,0)
    if bbsval1 = 1
        write(25,1)
        write(9,0)
def rdnoisesw()
    #Read noise switch status.
    read(22)
def wrnoisesw()
    #Change noise switch position.
def rdADch(ad)


