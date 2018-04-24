#Here to make python recognize this as a package
def MAKE_EMULATED():
	from iol import baseball
	from iol import pygpio
	from iol import adlib
	from cli import colors
	print(u"\u001b[31mSET IOLIB TO EMULATED MODE, NO REAL IO WILL BE MODIFIED\u001b[0m")
	pygpio.GPIOPin = pygpio.EmulatedGPIOPin 
	baseball.BaseballSwitch = baseball.EmulatedBaseballSwitch
	adlib.ADC = adlib.EmulatedADC