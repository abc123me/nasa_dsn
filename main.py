import sys
if(sys.version_info[0] < 3): #Check python version
	raise "This only supports python3!"

import iol
__EMULATING_NOISE_SOURCE = iol.IS_EMULATED()
__EMULATING_TRANSLATOR = iol.IS_EMULATED()

import time
from errors import StatusError
from iol.pygpio import GPIOPin
from cli import colors
from iol.baseball import BaseballSwitch
from iol.adlib import ADC

__attenuatorValue = "unknown"
__noiseSourceActive = False
__translatorActive = False

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
__translatorPathEnable = GPIOPin(10)
__noiseSourceEnable = GPIOPin(24)
#Set them all to outputs
__translatorPathEnable.setOutput()
__noiseSourceEnable.setOutput()
print(colors.green + "Success!" + colors.reset)
''' TRANSMIT LEVEL CONTROL BITS
28		*		Trans Level Ctl Bit 0	IDSC	   Signal Attn Bit 0 LSB   .25 dB
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
__transLevel = [GPIOPin(1), GPIOPin(5), GPIOPin(6), GPIOPin(12), GPIOPin(13), GPIOPin(19), GPIOPin(16), GPIOPin(26)]
for pin in __transLevel:
	pin.setOutput()
	pin.write(False)
print(colors.green + "Success!" + colors.reset)
''' TRANSLATOR AND NOISE CONTROL
Noise Status	    GPIO 22 	Noise ON
Translator Status	GPIO 23 	Translator Path ON

Relay Control 8	    GPIO 24 	Turns on Noise Source
Relay Control 7	    GPIO 10 	Turns on Translator path
'''
print(colors.yellow + "Initializing status pins..." + colors.reset)
noiseStatus = GPIOPin(22)
noiseStatus.isNegated = True #This pin is true LOW, so we flag it as that so when we read and write it interprets True as off, and FALSE as on
translatorStatus = GPIOPin(23)
noiseStatus.setInput()
translatorStatus.setInput()
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
print(colors.yellow + "Initializing baseball switch 1" + colors.reset)
#def __init__(self, name, settingA, settingB, positionA, positionB):
baseballSwitch1 = BaseballSwitch("BBSW1", 4, 14, 7, 0)
baseballSwitch1.initGPIO()
print(colors.green + "Success!" + colors.reset)
print(colors.yellow + "Initializing baseball switch 2" + colors.reset)
baseballSwitch2 = BaseballSwitch("BBSW2", 11, 8, 15, 17)
baseballSwitch2.initGPIO()
print(colors.green + "Success!" + colors.reset)
print(colors.yellow + "Initializing baseball switch 3" + colors.reset)
baseballSwitch3 = BaseballSwitch("BBSW3", 9, 25, 18, 27)
baseballSwitch3.initGPIO()
print(colors.green + "Success!" + colors.reset)

print(colors.yellow + "Initializing i2c ADC" + colors.reset)
adc = ADC(0)
adc.setup()
print(colors.green + "Success!" + colors.reset)
''' 
UTILITY FUNCTIONS FOR SETTING, GETTING AND GENERAL CONTROL
'''
print(colors.yellow + "Initializing utility functions..." + colors.reset)
def getAttenuatorValue():
	return __attenuatorValue
def isTranslatorOn():
	if(__EMULATING_TRANSLATOR):
		return __translatorActive
	return translatorStatus.digitalRead()
def isNoiseSourceOn():
	if(__EMULATING_NOISE_SOURCE):
		return __noiseSourceActive
	return noiseStatus.digitalRead()
def setTranslatorPath(enable): #Disables or enables the translator
	global __translatorActive
	if(enable):
		__translatorPathEnable.write(True)
		__translatorActive = True
		time.sleep(0.25)
		if(not isTranslatorOn()):
			__translatorPathEnable.write(False) #Stop trying to turn it on, since it will just risk damage
			print(colors.red + "Translator failed to turn on within 0.25s" + colors.reset)
			raise StatusError("Translator", "Did not turn on!")
	else:
		__translatorPathEnable.write(False)
		__translatorActive = False
		time.sleep(0.25)
		if(isTranslatorOn()):
			print(colors.red + "Translator failed to turn off within 0.25s" + colors.reset)
			raise StatusError("Translator", "Did not turn off!") 
def setNoiseSource(enable): #Disables or enables the noise source
	global __noiseSourceActive
	if(enable):
		__noiseSourceEnable.write(True)
		time.sleep(0.25)
		__noiseSourceActive = True
		if(not isNoiseSourceOn()):
			__noiseSourceEnable.write(False) #Stop trying to turn it on, since it will just risk damage
			print(colors.red + "Noise source failed to turn on within 0.25s" + colors.reset)
			raise StatusError("Noise source", "Did not turn on!")
	else:
		__noiseSourceEnable.write(False)
		time.sleep(0.25)
		__noiseSourceActive = False
		if(isNoiseSourceOn()):
			print(colors.red + "Noise source failed to turn off within 0.25s" + colors.reset)
			raise StatusError("Noise source", "Did not turn off!")
def decibelsToBinary(num): #Converts the decibel value input to the binary value output that needs to be written to the GPIO Pins
	val = [False] * 8 #initialized the array with 8 False values
	for i in range(7, -1, -1): #Start at the 8th bit and go down to the 0th bit, this dosen't start at the 7th bit and go to the -1st bit
		#mdbv is the result of raising 2 to the power of the difference of the iterator and 2
		#This puts mdbv in the range of 32 to .25 because 2 ^ -2 = 1 / 4 and 2 ^ 5 = 32 (aka Math)
		mdbv = 2 ** (i - 2)
		if(num >= mdbv): # If the number is greator than mdbv than subtract the number by it and set the current bit to true
			num = num - mdbv;
			val[i] = True
	return val
def setAttenuatorValue(db): #Sets the attenuator value to a specified decibel level
	if(db < 0 or db > 63.75): #Make sure the level is in range for the 8 bit buffer
		raise BufferError("Cannot set to " + str(db) + " because that exceeds the 8 bit buffer")
	val = decibelsToBinary(db)
	for i in range(0, 8): #First set them all to zero to make sure we don't accidentally transmit on a higher power then we want
		__transLevel[i].write(False)
	for i in range(0, 8): #This will set the lowest bits FIRST so the power will start off small and rise
		__transLevel[i].write(val[i])
	global __attenuatorValue
	__attenuatorValue = db #store the new value for later use with getAttenuatorValue
def toggleTranslator():
	setTranslatorPath(not isTranslatorOn())
def toggleNoiseSource():
	setNoiseSource(not isNoiseSourceOn())
def getAdcValue():
	return adc.getValue()
print(colors.green + "Success!" + colors.reset)
print(colors.yellow + "Setting attenuator to 0 dB..." + colors.reset)
setAttenuatorValue(0)
print(colors.green + "Success!" + colors.reset)
print(colors.yellow + "Turning off noise source..." + colors.reset)
setNoiseSource(False)
print(colors.green + "Success!" + colors.reset)
print(colors.yellow + "Turning off translator..." + colors.reset)
setTranslatorPath(False)
print(colors.green + "Success!" + colors.reset)
