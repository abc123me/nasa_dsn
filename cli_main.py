import time, cli
from errors import StatusError
from cli import colors
from cli.ui import clearTerm, menu, MenuEntry

if(__name__ != "__main__"):
  print(colors.red + "This cannot be used as a library, sorry!" + colors.reset)
  exit(1)

#Helkper method that converbs a boolean into an ON or OFF statement (thats colored for coolness)
def onOff(value):
	if(value):
		return colors.green + "ON" + colors.reset
	return colors.red + "OFF" + colors.reset

import main
#Baseball menu, when calls it creates a menu for the specified baseball switch
def baseballMenu(bb):
	def printPos():
		print("Baseball switch " + bb.name + " is at position: " + bb.getPosition().upper())
	def setPosA():
		bb.setPosition("a")
	def setPosB():
		bb.setPosition("b")
	while True:
		getSwitchPosition = MenuEntry(colors.cyan + "Get switch position" + colors.reset, event = printPos)
		swapPositions = MenuEntry(colors.cyan + "Swap switch position" + colors.reset, event = bb.swapPos, areYouSure = True)
		setPositionA = MenuEntry(colors.cyan + "Set switch position to A" + colors.reset, event = setPosA, areYouSure = True)
		setPositionB = MenuEntry(colors.cyan + "Set switch position to B" + colors.reset, event = setPosB, areYouSure = True)
		exit = MenuEntry(colors.red + "Leave the menu" + colors.reset)

		header = colors.yellow + "Baseball switch control" + colors.reset
		entries = [getSwitchPosition, swapPositions, setPositionA, setPositionB, exit]
		prompt = colors.yellow + "Select an option: " + colors.reset
		sel = menu(header, entries, prompt)

		if(sel == exit):
			return
#Main loop
while True:
	clearTerm()
	print(colors.reset, end = "")
	setAttenuator = MenuEntry(colors.cyan + "Set attenuator value (" + colors.blue + str(main.getAttenuatorValue()) + "dB" + colors.cyan + ")" + colors.reset)
	setTranslator = MenuEntry(colors.cyan + "Toggle translator (" + onOff(main.isTranslatorOn()) + colors.cyan + ")" + colors.reset, areYouSure = True, event = main.toggleTranslator)
	setNoise = MenuEntry(colors.cyan + "Toggle noise source (" + onOff(main.isNoiseSourceOn()) + colors.cyan + ")" + colors.reset, areYouSure = True, event = main.toggleNoiseSource)
	modifySwitch1 = MenuEntry(colors.yellow + "Modify BBSW1" + colors.reset)
	modifySwitch2 = MenuEntry(colors.yellow + "Modify BBSW2" + colors.reset)
	modifySwitch3 = MenuEntry(colors.yellow + "Modify BBSW3" + colors.reset)
	modifySwitch1.associatedSwitch = main.baseballSwitch1
	modifySwitch2.associatedSwitch = main.baseballSwitch2
	modifySwitch3.associatedSwitch = main.baseballSwitch3
	exitPrgm = MenuEntry(colors.red + "Exit the CLI" + colors.reset, event = exit)

	header = colors.yellow + "Main feed control" + colors.reset
	entries = [setAttenuator, modifySwitch1, modifySwitch2, modifySwitch3, setTranslator, setNoise, exitPrgm]
	prompt = colors.yellow + "Select an option: " + colors.reset
	sel = None
	try:
 		sel = menu(header, entries, prompt)
	except StatusError as error:
		print(str(error))
		if(not cli.ui.areYouSure(message = "Would you like to stay in the CLI [y/N]? ")):
			print(colors.red + "Exiting now!" + colors.reset)
			exit(1)
		continue;

	if(sel == modifySwitch1 or sel == modifySwitch2 or sel == modifySwitch3):
		baseballMenu(sel.associatedSwitch)
	if(sel == setAttenuator):
		valA = input("New attenuator value (dB): ")
		val = -1.0
		try:
			val = float(valA)
			if(val < 0 or val > 63.75):
				raise ValueError
		except ValueError:
			print(colors.red + "Must be a number between 0 and 63.75" + colors.reset)
			time.sleep(1)
			continue
		if(not cli.ui.areYouSure()):
			continue
		print(colors.yellow + "Updating attenuator value to " + str(val) + "dB" + colors.reset)
		main.setAttenuatorValue(val)
		print(colors.green + "Sucess!" + colors.reset)
