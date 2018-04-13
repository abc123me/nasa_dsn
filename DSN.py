import time
import smbus
import pygpio
import adlib

''' RELAY CONTROL PINS
18		*		Relay Control 8	GPIO 24	Turns on Noise Source
19		*		Relay Control 7	GPIO 10	Turns on Translator path
20	GND					
21		*		Relay Control 6	GPIO 9	BBSW 3 A setting
22		*		Relay Control 5	GPIO 25	BBSW 3 B setting
23		*		Relay Control 4	GPIO 11	BBSW 2 A setting
24		*		Relay Control 3	GPIO 8	BBSW 2 B setting
25	GND					
26		*		Relay Control 2	GPIO 7	BBSW 1 A setting
27		*		Relay Control 1	IDSD	BBSW 1 B setting
'''
print("Initializing relay pins... ")
relayCtrl = [ #Initialize as an array for easier addressing
    pygpio.GPIOPin(IDSD), #Apparently this goes to the IDSD pin, to my knowledge this pin cannot be used as GPIO? 
    pygpio.GPIOPin(7), 
    pygpio.GPIOPin(8), 
    pygpio.GPIOPin(11), 
    pygpio.GPIOPin(25), 
    pygpio.GPIOPin(9), 
    pygpio.GPIOPin(10), 
    pygpio.GPIOPin(24)]
for pin in relayCtrl:
    pin.setOutput()
    
''' TRANSMIT LEVEL CONTROL BITS
28		*		Trans Level Ctl Bit 0	IDSC	 Signal Attn Bit 0 LSB   .25 dB
29		*		Trans Level Ctl Bit 1	GPIO 5 	 Signal Attn Bit 1       .5 dB
30	GND					
31		*		Trans Level Ctl Bit 2	GPIO 6	 Signal Attn Bit 2       1 dB
32		*		Trans Level Ctl Bit 3	GPIO 12	 Signal Attn Bit 3       2 dB
33		*		Trans Level Ctl Bit 4	GPIO 13	 Signal Attn Bit 4       4 dB
34	GND					
35		*		Trans Level Ctl Bit 5	GPIO 19  Signal Attn Bit 5       8 dB
36		*		Trans Level Ctl Bit 6	GPIO 16	 Signal Attn Bit 6       16 dB
37		*		Trans Level Ctl Bit 7	GPIO 26	 Signal Attn Bit 7 MSB   32 dB
'''
transLevel = [ 
    pygpio.GPIOPin(IDSC), #Apparently this goes to the IDSC pin, to my knowledge this pin cannot be used as GPIO? 
    pygpio.GPIOPin(5), 
    pygpio.GPIOPin(6), 
    pygpio.GPIOPin(12), 
    pygpio.GPIOPin(13), 
    pygpio.GPIOPin(19), 
    pygpio.GPIOPin(16), 
    pygpio.GPIOPin(25)]
for pin in transLevel:
    pin.setOutput()
def decibelsToBinary(num):
	val = [False] * 8
	for i in range(7, -1, -1):
		mdbv = 2 ** (i - 2)
		if(num >= mdbv):
			num = num - mdbv;
			val[i] = True
	return val
def setTransmitLevel(db):
    val = [False] * 8
	for i in range(7, -1, -1):
		mdbv = 2 ** (i - 2)
		if(num >= mdbv):
			num = num - mdbv;
			val[i] = True
    for i in range(0, 8):
        transLevel[i].write(val[i])
        
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

