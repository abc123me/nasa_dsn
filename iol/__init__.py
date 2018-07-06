#Here to make python recognize this as a package
from iol import baseball
from iol import pygpio
from iol import adlib
from cli import colors
__old_gpio = pygpio.GPIOPin
__old_bb = baseball.BaseballSwitch
__old_adc = adlib.ADC
__emulated = False

def SET_EMULATED(mode):
	if(mode):
		print(u"\u001b[31mSET IOLIB TO EMULATED MODE, NO REAL IO WILL BE MODIFIED\u001b[0m")
		pygpio.GPIOPin = pygpio.EmulatedGPIOPin 
		baseball.BaseballSwitch = baseball.EmulatedBaseballSwitch
		adlib.ADC = adlib.EmulatedADC
		__emulated = True
	else:
		print(u"\u001b[31mSET IOLIB TO NON-EMULATED MODE, REAL IO WILL BE MODIFIED\u001b[0m")
		pygpio.GPIOPin = __old_gpio
		baseball.BaseballSwitch = __old_bb
		adlib.ADC = __old_adc
		__emulated = False
def MAKE_EMULATED():
	SET_EMULATED(True)
def IS_EMULATED():
	return __emulated