import sys
if(sys.version_info[0] < 3): #Check python version
	raise "This only supports python3!"

import time
#from pygpio import EmulatedGPIOPin as GPIOPin
from pygpio import GPIOPin as GPIOPin
import utils
import colors
from iolib import BaseballSwitch

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
print(colors.yellow + "Initializing relay control pins... " + colors.reset)
baseballSwitch1B = GPIOPin(0)
baseballSwitch1A = GPIOPin(7)
baseballSwitch2B = GPIOPin(8)
baseballSwitch2A = GPIOPin(11)
baseballSwitch3B = GPIOPin(25)
baseballSwitch3A = GPIOPin(9)
translatorPathEnable = GPIOPin(10)
noiseSourceEnable = GPIOPin(24)
#Set them all to outputs
baseballSwitch1A.setOutput()
baseballSwitch1B.setOutput()
baseballSwitch2A.setOutput()
baseballSwitch2B.setOutput()
baseballSwitch3A.setOutput()
baseballSwitch3B.setOutput()
translatorPathEnable.setOutput()
noiseSourceEnable.setOutput()
print(colors.green + "Success!" + colors.reset)
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
print(colors.yellow + "Initializing transmit level pins..." + colors.reset)
transLevel = [GPIOPin(1), GPIOPin(5), GPIOPin(6), GPIOPin(12), GPIOPin(13), GPIOPin(19), GPIOPin(16), GPIOPin(26)]
for pin in transLevel:
	pin.setOutput()
	pin.write(False)
def setTransmitLevel(db):
	if(db < 0 or db > 63.75):
		raise BufferError("Cannot set to " + str(db) + " because that exceeds the 8 bit buffer")
	val = utils.decibelsToBinary(db)
	for i in range(0, 8): #First set them all to zero to make sure we don't accidentally transmit on a higher power then we want
		transLevel[i].write(False)
	for i in range(0, 8): #This will set the lowest bits FIRST so the power will start off small and rise
		transLevel[i].write(val[i])
print(colors.green + "Success!" + colors.reset)
print(colors.yellow + "Setting attenuator to 0 dB..." + colors.reset)
setTransmitLevel(0)
print(colors.green + "Success!" + colors.reset)
''' TRANSLATOR AND NOISE CONTROL
Noise Status	    GPIO 22 	Noise ON
Translator Status	GPIO 23 	Translator Path ON
		
Relay Control 8	    GPIO 24 	Turns on Noise Source     
Relay Control 7	    GPIO 10 	Turns on Translator path  
'''
print(colors.yellow + "Initializing status pins..." + colors.reset)
noiseStatus = GPIOPin(22)
noiseStatus.isNegated = True #This pin is true HIGH, so we flag it as that so when we read and write it interprets True as off, and FALSE as on
translatorStatus = GPIOPin(23)
noiseStatus.setInput()
translatorStatus.setInput()
def setTranslatorPath(enable):
	if(enable):
		translatorPathEnable.write(True)
		time.sleep(0.25)
		if(not translatorStatus.digitalRead()):
			print(colors.red + "Translator failed to turn on within 0.25s" + colors.reset)
			raise "Translator did not turn on!"
	else:
		translatorPathEnable.write(False)
		time.sleep(0.25)
		if(translatorStatus.digitalRead()):
			print(colors.red + "Translator failed to turn off within 0.25s" + colors.reset)
			raise "Translator did not turn off, did the relay contacts weld together?"
def setNoiseSource(enable):
	if(enable):
		noiseSourceEnable.write(True)
		time.sleep(0.25)
		if(not noiseStatus.digitalRead()):
			print(colors.red + "Noise source failed to turn on within 0.25s" + colors.reset)
			raise "Noise source did not turn on!"
	else:
		noiseSourceEnable.write(False)
		time.sleep(0.25)
		if(noiseStatus.digitalRead()):
			print(colors.red + "Noise source failed to turn off within 0.25s" + colors.reset)
			raise "Noise source did not turn off, did the relay contacts weld together?"
print(colors.green + "Success!" + colors.reset)
''' BASEBALL SWITCH CONTROL
=============CONTROL PINS=================================
26		*		Relay Control 2	GPIO 7		BBSW 1 A setting
27		*		Relay Control 1	IDSD GPIO 0	BBSW 1 B setting
23		*		Relay Control 4	GPIO 11		BBSW 2 A setting
24		*		Relay Control 3	GPIO 8		BBSW 2 B setting
21		*		Relay Control 6	GPIO 9		BBSW 3 A setting
22		*		Relay Control 5	GPIO 25		BBSW 3 B setting
=============STATISTICS===================================
7			*	BBSW1  Stat 1	GPIO 4		BBSW 1 Pos A
8			*	BBSW1  Stat 2	GPIO 14		BBSW 1 Pos B
10			*	BBSW2  Stat 1	GPIO 15		BBSW 2 Pos A
11			*	BBSW2  Stat 2	GPIO 17		BBSW 2 Pos B
12			*	BBSW3  Stat 1	GPIO 18		BBSW 3 Pos A
13			*	BBSW3  Stat 2	GPIO 27		BBSW 3 Pos B
'''
print(colors.yellow + "Initializing baseball switch logic..." + colors.reset)

#def __init__(self, name, settingA, settingB, positionA, positionB):
baseballSwitch1 = BaseballSwitch("BBSW1", GPIOPin(4), GPIOPin(14), GPIOPin(7), GPIOPin(0))
baseballSwitch1.initGPIO()
baseballSwitch2 = BaseballSwitch("BBSW2", GPIOPin(11), GPIOPin(8), GPIOPin(15), GPIOPin(17))
baseballSwitch2.initGPIO()
baseballSwitch3 = BaseballSwitch("BBSW3", GPIOPin(9), GPIOPin(25), GPIOPin(18), GPIOPin(27))
baseballSwitch3.initGPIO()
print(colors.green + "Success!" + colors.reset)
